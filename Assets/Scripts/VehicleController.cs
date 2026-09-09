using UnityEngine;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif

/// <summary>Moves the whole driver vehicle rig by keyboard or toward an assigned navigation target.</summary>
public class VehicleController : MonoBehaviour
{
    [SerializeField] private float driveSpeed = 7f;
    [SerializeField] private float reverseSpeed = 3f;
    [SerializeField] private float turnSpeed = 95f;
    [SerializeField] private float arrivalDistance = 2.2f;

    public Transform NavigationTarget { get; private set; }
    public bool AutoNavigate { get; private set; }
    public bool HasArrived => NavigationTarget != null && Vector3.Distance(transform.position.FlattenY(), NavigationTarget.position.FlattenY()) <= arrivalDistance;

    private void Update()
    {
        float forward = 0f;
        float turn = 0f;
#if ENABLE_INPUT_SYSTEM
        if (Keyboard.current != null)
        {
            forward = (Keyboard.current.wKey.isPressed ? 1f : 0f) - (Keyboard.current.sKey.isPressed ? 1f : 0f);
            turn = (Keyboard.current.dKey.isPressed ? 1f : 0f) - (Keyboard.current.aKey.isPressed ? 1f : 0f);
            if (Mathf.Abs(forward) > 0f || Mathf.Abs(turn) > 0f) AutoNavigate = false;
        }
#else
        forward = Input.GetAxisRaw("Vertical");
        turn = Input.GetAxisRaw("Horizontal");
        if (Mathf.Abs(forward) > 0f || Mathf.Abs(turn) > 0f) AutoNavigate = false;
#endif

        if (AutoNavigate && NavigationTarget != null && !HasArrived)
        {
            Vector3 direction = (NavigationTarget.position - transform.position).FlattenY();
            Quaternion look = Quaternion.LookRotation(direction.normalized, Vector3.up);
            transform.rotation = Quaternion.RotateTowards(transform.rotation, look, turnSpeed * 1.7f * Time.deltaTime);
            transform.position += transform.forward * driveSpeed * Time.deltaTime;
            return;
        }

        transform.Rotate(0f, turn * turnSpeed * Time.deltaTime, 0f);
        float speed = forward >= 0f ? driveSpeed : reverseSpeed;
        transform.position += transform.forward * forward * speed * Time.deltaTime;
    }

    public void SetNavigation(Transform target, bool autoStart)
    {
        NavigationTarget = target;
        AutoNavigate = autoStart;
    }

    public void ToggleAutoNavigation()
    {
        if (NavigationTarget != null && !HasArrived) AutoNavigate = !AutoNavigate;
    }

    public void Stop()
    {
        AutoNavigate = false;
        NavigationTarget = null;
    }
}

public static class VectorExtensions
{
    public static Vector3 FlattenY(this Vector3 value) => new Vector3(value.x, 0f, value.z);
}
