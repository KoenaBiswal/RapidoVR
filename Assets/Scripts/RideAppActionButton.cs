using UnityEngine;
using UnityEngine.UI;

/// <summary>Small bridge from the on-screen driver-app buttons to the ride workflow.</summary>
public class RideAppActionButton : MonoBehaviour
{
    public enum Action { OnlineOrRequest, Accept, ToggleAutoNavigate, Pickup, Complete }

    [SerializeField] private RideWorkflowManager workflow;
    [SerializeField] private Action action;

    private void Awake()
    {
        var button = GetComponent<Button>();
        if (button != null) button.onClick.AddListener(Press);
    }

    public void Press()
    {
        if (workflow == null) return;
        switch (action)
        {
            case Action.OnlineOrRequest: workflow.ReceiveRequest(); break;
            case Action.Accept: workflow.AcceptRide(); break;
            case Action.ToggleAutoNavigate:
                var vehicle = FindFirstObjectByType<VehicleController>();
                if (vehicle != null) vehicle.ToggleAutoNavigation();
                break;
            case Action.Pickup: workflow.PickUp(); break;
            case Action.Complete: workflow.CompleteTrip(); break;
        }
    }
}
