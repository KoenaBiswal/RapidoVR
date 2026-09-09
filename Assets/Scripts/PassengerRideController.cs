using UnityEngine;

/// <summary>Controls the passenger's visible wait, boarding and drop-off transitions.</summary>
public class PassengerRideController : MonoBehaviour
{
    [SerializeField] private Transform waitingSpot;
    [SerializeField] private Transform bikeSeat;
    [SerializeField] private Transform dropoffSpot;
    [SerializeField] private Vector3 seatedLocalPosition = new Vector3(0f, 0.64f, -0.74f);
    [SerializeField] private Vector3 seatedLocalEulerAngles = new Vector3(0f, 0f, 0f);

    public bool IsOnBike { get; private set; }

    public void ResetToWaiting()
    {
        transform.SetParent(null, true);
        transform.position = waitingSpot.position;
        transform.rotation = waitingSpot.rotation;
        gameObject.SetActive(true);
        IsOnBike = false;
    }

    public void Board()
    {
        // The imported Remy FBX contains only a standing pose.  Hiding that pose while
        // onboard is more believable than displaying a full-height standing passenger
        // through the motorcycle.  It becomes visible again at the destination.
        gameObject.SetActive(false);
        IsOnBike = true;
    }

    public void DropOff()
    {
        transform.SetParent(null, true);
        transform.position = dropoffSpot.position;
        transform.rotation = dropoffSpot.rotation;
        gameObject.SetActive(true);
        IsOnBike = false;
    }
}
