using System.Collections;
using UnityEngine;
using UnityEngine.UI;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

/// <summary>
/// Drives the small, keyboard-testable driver workflow used in the mid-evaluation demo.
/// The public methods are separate from keyboard input so VR controller buttons can call them later.
/// </summary>
public class DriverWorkflowController : MonoBehaviour
{
    public enum DriverStage
    {
        DriverOnline = 1,
        RideRequestReceived = 2,
        DriverAcceptsRide = 3,
        NavigateToPickup = 4,
        PassengerPickup = 5,
        NavigateToDestination = 6,
        TripCompleted = 7
    }

    [Header("UI references")]
    [SerializeField] private Text statusText;
    [SerializeField] private Text requestText;
    [SerializeField] private Text pickupText;
    [SerializeField] private Text destinationText;
    [SerializeField] private Text stageText;
    [SerializeField] private Text instructionText;

    [Header("Ride information")]
    [SerializeField] private string pickupLocation = "College Main Gate";
    [SerializeField] private string destinationLocation = "City Library";

    [SerializeField] private DriverStage currentStage = DriverStage.DriverOnline;
    [Header("Scooter movement")]
    [SerializeField] private Transform scooter;
    [SerializeField] private Transform pickupMarker;
    [SerializeField] private Transform destinationMarker;
    [SerializeField] private Transform passenger;
    [SerializeField] private Transform passengerSeat;
    [SerializeField] private float interactionDistance = 7.5f;
    [SerializeField] private float autoDriveSpeed = 5.5f;
    [SerializeField] private float manualDriveSpeed = 6f;
    [SerializeField] private float turnSpeed = 90f;

    private Coroutine transitionRoutine;
    private bool autoDriving;

    // Other future systems (for example, XR controller buttons) can read this safely.
    public DriverStage CurrentStage => currentStage;

    private void Start()
    {
        UpdateDisplay();
    }

    private void Update()
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            if (Keyboard.current.rKey.wasPressedThisFrame) ReceiveRideRequest();
            if (Keyboard.current.aKey.wasPressedThisFrame) AcceptRide();
            if (Keyboard.current.pKey.wasPressedThisFrame) PickUpPassenger();
            if (Keyboard.current.tKey.wasPressedThisFrame) CompleteTrip();
        }
#else
        if (Input.GetKeyDown(KeyCode.R)) ReceiveRideRequest();
        if (Input.GetKeyDown(KeyCode.A)) AcceptRide();
        if (Input.GetKeyDown(KeyCode.P)) PickUpPassenger();
        if (Input.GetKeyDown(KeyCode.T)) CompleteTrip();
#endif

        DriveScooter();
    }

    // These four methods can later be connected to XR controller UI buttons or interactable objects.
    public void ReceiveRideRequest()
    {
        if (currentStage != DriverStage.DriverOnline) return;
        SetStage(DriverStage.RideRequestReceived);
    }

    public void AcceptRide()
    {
        if (currentStage != DriverStage.RideRequestReceived) return;
        SetStage(DriverStage.DriverAcceptsRide);
        StartTimedTransition(DriverStage.NavigateToPickup);
    }

    public void PickUpPassenger()
    {
        if (currentStage != DriverStage.NavigateToPickup) return;
        if (!IsNear(scooter, passenger, interactionDistance)) return;
        SetStage(DriverStage.PassengerPickup);
        // For this prototype, pressing P boards the passenger onto the rear seat.
        if (passenger != null && passengerSeat != null)
        {
            passenger.SetParent(passengerSeat, false);
            passenger.localPosition = Vector3.zero;
            passenger.localRotation = Quaternion.identity;
        }
        StartTimedTransition(DriverStage.NavigateToDestination);
    }

    public void CompleteTrip()
    {
        if (currentStage != DriverStage.NavigateToDestination) return;
        if (!IsNear(scooter, destinationMarker, interactionDistance)) return;
        SetStage(DriverStage.TripCompleted);
    }

    private static bool IsNear(Transform first, Transform second, float distance)
    {
        return first != null && second != null && Vector3.Distance(first.position, second.position) <= distance;
    }

    private void StartTimedTransition(DriverStage nextStage)
    {
        if (transitionRoutine != null) StopCoroutine(transitionRoutine);
        transitionRoutine = StartCoroutine(TransitionAfterShortPause(nextStage));
    }

    private IEnumerator TransitionAfterShortPause(DriverStage nextStage)
    {
        yield return new WaitForSeconds(1.5f);
        SetStage(nextStage);
    }

    private void SetStage(DriverStage stage)
    {
        currentStage = stage;
        // The scooter automatically follows the simple route during each navigation stage.
        autoDriving = stage == DriverStage.NavigateToPickup || stage == DriverStage.NavigateToDestination;
        UpdateDisplay();
    }

    private void DriveScooter()
    {
        if (scooter == null) return;

        bool isNavigating = currentStage == DriverStage.NavigateToPickup || currentStage == DriverStage.NavigateToDestination;
        if (!isNavigating) return;

        Transform target = currentStage == DriverStage.NavigateToPickup ? pickupMarker : destinationMarker;
        if (target != null && autoDriving)
        {
            Vector3 targetPosition = target.position;
            targetPosition.y = scooter.position.y;
            Vector3 direction = targetPosition - scooter.position;
            if (direction.sqrMagnitude > 0.35f)
            {
                Quaternion targetRotation = Quaternion.LookRotation(direction.normalized, Vector3.up);
                scooter.rotation = Quaternion.RotateTowards(scooter.rotation, targetRotation, turnSpeed * Time.deltaTime * 2f);
                scooter.position += scooter.forward * autoDriveSpeed * Time.deltaTime;
            }
            else
            {
                autoDriving = false;
            }
        }

#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current == null) return;
        float forward = (Keyboard.current.wKey.isPressed ? 1f : 0f) - (Keyboard.current.sKey.isPressed ? 1f : 0f);
        float turn = (Keyboard.current.dKey.isPressed ? 1f : 0f) - (Keyboard.current.aKey.isPressed ? 1f : 0f);
#else
        float forward = Input.GetAxisRaw("Vertical");
        float turn = Input.GetAxisRaw("Horizontal");
#endif
        if (Mathf.Abs(forward) > 0.01f || Mathf.Abs(turn) > 0.01f)
        {
            autoDriving = false;
            scooter.Rotate(0f, turn * turnSpeed * Time.deltaTime, 0f);
            scooter.position += scooter.forward * forward * manualDriveSpeed * Time.deltaTime;
        }
    }

    private void UpdateDisplay()
    {
        string stageName = FormatStageName(currentStage);
        if (statusText != null) statusText.text = "DRIVER STATUS: " + GetStatusMessage();
        if (requestText != null) requestText.text = currentStage == DriverStage.DriverOnline ? "RIDE REQUEST: Waiting for request" : "RIDE REQUEST: Passenger ride request active";
        if (pickupText != null) pickupText.text = "PICKUP: " + pickupLocation;
        if (destinationText != null) destinationText.text = "DESTINATION: " + destinationLocation;
        if (stageText != null) stageText.text = "CURRENT STAGE " + (int)currentStage + "/7: " + stageName;
        if (instructionText != null) instructionText.text = GetInstruction();
    }

    private string GetStatusMessage()
    {
        switch (currentStage)
        {
            case DriverStage.DriverOnline: return "ONLINE — ready for rides";
            case DriverStage.RideRequestReceived: return "REQUEST RECEIVED — accept the ride";
            case DriverStage.DriverAcceptsRide: return "RIDE ACCEPTED";
            case DriverStage.NavigateToPickup: return "NAVIGATING TO PICKUP";
            case DriverStage.PassengerPickup: return "PASSENGER PICKED UP";
            case DriverStage.NavigateToDestination: return "NAVIGATING TO DESTINATION";
            case DriverStage.TripCompleted: return "TRIP COMPLETED — payment recorded";
            default: return "ONLINE";
        }
    }

    private string GetInstruction()
    {
        switch (currentStage)
        {
            case DriverStage.DriverOnline: return "Press R to receive a ride request";
            case DriverStage.RideRequestReceived: return "Press A to accept the ride";
            case DriverStage.NavigateToPickup: return "Reach the passenger at the yellow marker, then press P to board them. W/S/A/D can take manual control.";
            case DriverStage.NavigateToDestination: return "Reach the red destination marker, then press T to complete the trip. W/S/A/D can take manual control.";
            case DriverStage.TripCompleted: return "Demo complete. Stop and explain the completed workflow.";
            default: return "Updating driver workflow...";
        }
    }

    private static string FormatStageName(DriverStage stage)
    {
        switch (stage)
        {
            case DriverStage.DriverOnline: return "Driver Online";
            case DriverStage.RideRequestReceived: return "Ride Request Received";
            case DriverStage.DriverAcceptsRide: return "Driver Accepts Ride";
            case DriverStage.NavigateToPickup: return "Navigate to Pickup Location";
            case DriverStage.PassengerPickup: return "Passenger Pickup";
            case DriverStage.NavigateToDestination: return "Navigate to Destination";
            case DriverStage.TripCompleted: return "Trip Completed";
            default: return stage.ToString();
        }
    }
}
