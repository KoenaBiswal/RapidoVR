using UnityEngine;
using UnityEngine.UI;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

/// <summary>Owns the complete 11-stage bike-taxi lifecycle and updates the demonstration UI.</summary>
public class RideWorkflowManager : MonoBehaviour
{
    public enum Stage { OfflineReady, Online, Request, Accepted, NavigatePickup, ArrivedPickup, PassengerBoarded, NavigateDestination, ArrivedDestination, PassengerDroppedOff, Completed }

    [SerializeField] private VehicleController vehicle;
    [SerializeField] private PassengerRideController passenger;
    [SerializeField] private Transform pickup;
    [SerializeField] private Transform destination;
    [SerializeField] private GameObject pickupBeacon;
    [SerializeField] private GameObject destinationBeacon;
    [SerializeField] private Text statusText;
    [SerializeField] private Text stageText;
    [SerializeField] private Text phoneText;
    [SerializeField] private Text instructionText;
    [SerializeField] private Text distanceText;
    [SerializeField] private float fare = 125f;
    [SerializeField] private float tripDistanceKm = 2.6f;
    [SerializeField] private Stage stage = Stage.OfflineReady;

    private void Start()
    {
        // Always begin a demonstration with the passenger visibly waiting at pickup.
        if (passenger != null) passenger.ResetToWaiting();
        ApplyStage(Stage.OfflineReady);
    }
    private void Update()
    {
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            if (Keyboard.current.rKey.wasPressedThisFrame) ReceiveRequest();
            if (Keyboard.current.aKey.wasPressedThisFrame) AcceptRide();
            if (Keyboard.current.nKey.wasPressedThisFrame) vehicle.ToggleAutoNavigation();
            if (Keyboard.current.pKey.wasPressedThisFrame) PickUp();
            if (Keyboard.current.tKey.wasPressedThisFrame) CompleteTrip();
        }
#endif
        if (stage == Stage.NavigatePickup && vehicle.HasArrived) ApplyStage(Stage.ArrivedPickup);
        if (stage == Stage.NavigateDestination && vehicle.HasArrived) ApplyStage(Stage.ArrivedDestination);
        UpdateDistances();
    }

    public void ReceiveRequest() { if (stage == Stage.OfflineReady) ApplyStage(Stage.Online); else if (stage == Stage.Online) ApplyStage(Stage.Request); }
    public void AcceptRide() { if (stage == Stage.Request) { ApplyStage(Stage.Accepted); ApplyStage(Stage.NavigatePickup); } }
    public void PickUp() { if (stage == Stage.ArrivedPickup) { passenger.Board(); ApplyStage(Stage.PassengerBoarded); ApplyStage(Stage.NavigateDestination); } }
    public void CompleteTrip() { if (stage == Stage.ArrivedDestination) { passenger.DropOff(); ApplyStage(Stage.PassengerDroppedOff); ApplyStage(Stage.Completed); } }

    private void ApplyStage(Stage next)
    {
        stage = next;
        bool atPickup = next == Stage.NavigatePickup || next == Stage.ArrivedPickup;
        bool toDestination = next == Stage.NavigateDestination || next == Stage.ArrivedDestination;
        pickupBeacon.SetActive(atPickup);
        destinationBeacon.SetActive(toDestination || next >= Stage.PassengerBoarded);
        if (next == Stage.NavigatePickup) vehicle.SetNavigation(pickup, true);
        else if (next == Stage.NavigateDestination) vehicle.SetNavigation(destination, true);
        else if (next == Stage.Completed) vehicle.Stop();
        RefreshUI();
    }

    private void RefreshUI()
    {
        stageText.text = "STAGE " + ((int)stage + 1) + "/11 · " + Pretty(stage);
        statusText.text = stage == Stage.OfflineReady ? "DRIVER STATUS · OFFLINE / READY" : stage == Stage.Completed ? "DRIVER STATUS · ONLINE / AVAILABLE" : "DRIVER STATUS · ONLINE";
        instructionText.text = "CONTROLS\nR Online / request · A Accept · N Auto Navigate\nWASD Drive · P Pick up · T Complete";
        phoneText.text = PhoneContent();
    }

    private void UpdateDistances()
    {
        Transform target = stage == Stage.NavigatePickup || stage == Stage.ArrivedPickup ? pickup : destination;
        float meters = vehicle == null || target == null ? 0f : Vector3.Distance(vehicle.transform.position.FlattenY(), target.position.FlattenY());
        distanceText.text = "NAVIGATION · " + meters.ToString("0") + " m";
    }

    private string PhoneContent()
    {
        if (stage == Stage.OfflineReady) return "RIDE DRIVER\n\nYou are offline.\nPress R to go online.";
        if (stage == Stage.Online) return "RIDE DRIVER\n\nONLINE · Waiting for nearby rides\nPress R to receive request.";
        if (stage == Stage.Request) return "INCOMING RIDE\n\nPickup: College Main Gate\nDrop: City Library\nDistance: " + tripDistanceKm + " km\nFare: ₹" + fare + "\n\n[A] ACCEPT     [Reject unavailable]";
        if (stage == Stage.NavigatePickup || stage == Stage.ArrivedPickup) return "NAVIGATE TO PICKUP\n\nCollege Main Gate\nPassenger is waiting\n\n[N] AUTO NAVIGATE · [P] BOARD";
        if (stage == Stage.NavigateDestination || stage == Stage.ArrivedDestination) return "RIDE IN PROGRESS\n\nDestination: City Library\nFare: ₹" + fare + "\n\n[N] AUTO NAVIGATE · [T] DROP OFF";
        if (stage == Stage.Completed) return "TRIP COMPLETED\n\nDistance: " + tripDistanceKm + " km\nFare earned: ₹" + fare + "\n\nYou are now available for rides.";
        return "RIDE DRIVER\nUpdating trip...";
    }

    private static string Pretty(Stage value)
    {
        string text = value.ToString();
        for (int i = 1; i < text.Length; i++) if (char.IsUpper(text[i])) text = text.Insert(i++, " ");
        return text;
    }
}
