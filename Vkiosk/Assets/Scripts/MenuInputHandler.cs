using UniRx;
using UnityEngine;

public class MenuInputHandler : MonoBehaviour
{
    public MenuSpinningManager menuManager;

    private Vector2 lastMousePos;
    private bool isDragging = false;

    void Start()
    {
        Observable.EveryUpdate()
            .Where(_ => Input.GetMouseButtonDown(0))
            .Subscribe(_ =>
            {
                isDragging = true;
                lastMousePos = Input.mousePosition;
            });

        Observable.EveryUpdate()
            .Where(_ => isDragging)
            .Subscribe(_ =>
            {
                Vector2 currentMousePos = Input.mousePosition;
                float delta = currentMousePos.x - lastMousePos.x;
                lastMousePos = currentMousePos;

                menuManager.ApplyDrag(delta);
            });


        Observable.EveryUpdate()
            .Where(_ => Input.GetMouseButtonUp(0))
            .Subscribe(_ =>
            {
                isDragging = false;
                menuManager.StartDecayAndSnap();
            });

    }
}
