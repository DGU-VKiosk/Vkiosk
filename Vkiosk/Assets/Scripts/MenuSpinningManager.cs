using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MenuSpinningManager : MonoBehaviour
{
    public Transform centerPoint;
    public List<Transform> menuItems = new List<Transform>();
    private float radius = 20f;
    private float rotationSpeed = 0f;
    private float dragSensitivity = 0.1f;
    private float decayRate = 1f;

    private float[] targetAngles;
    private float currentRotation = 0f;

    private Coroutine decayRoutine;

    void Start()
    {
        int count = menuItems.Count;
        targetAngles = new float[count];

        for (int i = 0; i < count; i++)
            targetAngles[i] = (360f / count) * i;

        UpdateMenuItemPositions();
    }

    public void ApplyDrag(float dragDelta)
    {
        float deltaRotation = -dragDelta * dragSensitivity;
        currentRotation += deltaRotation;
        UpdateMenuItemPositions();
    }

    public void StartDecayAndSnap()
    {
        if (decayRoutine != null) StopCoroutine(decayRoutine);
        decayRoutine = StartCoroutine(RotationDecayAndSnap());
    }

    private IEnumerator RotationDecayAndSnap()
    {
        while (Mathf.Abs(rotationSpeed) > 0.05f)
        {
            currentRotation += rotationSpeed;
            rotationSpeed = Mathf.Lerp(rotationSpeed, 0f, Time.deltaTime * decayRate);
            UpdateMenuItemPositions();
            yield return null;
        }

        yield return StartCoroutine(SnapCoroutine());
        decayRoutine = null;
    }

    void UpdateMenuItemPositions()
    {
        float minDistance = float.MaxValue;
        int selectedIndex = 0;

        for (int i = 0; i < menuItems.Count; i++)
        {
            float angleDeg = targetAngles[i] + currentRotation;
            float angleRad = angleDeg * Mathf.Deg2Rad;

            Vector3 newPos = new Vector3(
                centerPoint.position.x + Mathf.Sin(angleRad) * radius,
                centerPoint.position.y,
                centerPoint.position.z + Mathf.Cos(angleRad) * radius
            );
            menuItems[i].position = newPos;

            float angleToCenter = Mathf.Abs(Mathf.DeltaAngle(currentRotation, targetAngles[i]));
            if (angleToCenter < minDistance)
            {
                minDistance = angleToCenter;
                selectedIndex = i;
            }
        }
    }

    public void RotateBySpeedInstant()
    {
        currentRotation += rotationSpeed;
        UpdateMenuItemPositions();
    }

    private Coroutine snapCoroutine;

    public void SnapToNearestSlot()
    {
        if (snapCoroutine != null) StopCoroutine(snapCoroutine);
        snapCoroutine = StartCoroutine(SnapCoroutine());
    }

    private IEnumerator SnapCoroutine()
    {
        float velocity = 0f;
        float minDiff = 360f;
        float targetOffset = 0f;

        foreach (float target in targetAngles)
        {
            float diff = Mathf.DeltaAngle(currentRotation, target);
            if (Mathf.Abs(diff) < Mathf.Abs(minDiff))
            {
                minDiff = diff;
                targetOffset = target;
            }
        }

        while (Mathf.Abs(Mathf.DeltaAngle(currentRotation, targetOffset)) > 0.1f)
        {
            currentRotation = Mathf.SmoothDampAngle(currentRotation, targetOffset, ref velocity, 0.1f); // 감속 시간 조정
            UpdateMenuItemPositions();
            yield return null;
        }

        currentRotation = targetOffset;
        UpdateMenuItemPositions();
        snapCoroutine = null;
    }
}