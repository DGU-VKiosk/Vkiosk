using UniRx;
using UnityEngine;

public enum MenuState { Category, Menu }

public class MenuInputHandler : MonoBehaviour
{
    public System.Action OnSwipeUp;
    public System.Action OnSwipeDown;

    private enum DragDirection { None, Horizontal, Vertical }
    private DragDirection currentDragDirection = DragDirection.None;

    private Vector2 lastMousePos;
    private bool isDragging = false;
    private float directionLockThreshold = 10f;

    public MenuSpinningManager categoryManager;
    public MenuSpinningManager itemManager;
    private MenuState currentState = MenuState.Category;

    public void SetState(MenuState state)
    {
        currentState = state;
    }

    private MenuSpinningManager ActiveManager =>
        currentState == MenuState.Category ? categoryManager : itemManager;

    void Start()
    {
        // 드래그 시작
        Observable.EveryUpdate()
            .Where(_ => Input.GetMouseButtonDown(0))
            .Subscribe(_ =>
            {
                isDragging = true;
                lastMousePos = Input.mousePosition;
                currentDragDirection = DragDirection.None;
            });

        // 드래그 중
        Observable.EveryUpdate()
            .Where(_ => isDragging)
            .Subscribe(_ =>
            {
                Vector2 currentMousePos = Input.mousePosition;
                Vector2 delta = currentMousePos - lastMousePos;

                // 방향 판단
                if (currentDragDirection == DragDirection.None)
                {
                    if (delta.magnitude > directionLockThreshold)
                    {
                        currentDragDirection = Mathf.Abs(delta.x) > Mathf.Abs(delta.y)
                            ? DragDirection.Horizontal
                            : DragDirection.Vertical;
                    }
                }

                // 방향에 따라 동작
                if (currentDragDirection == DragDirection.Horizontal)
                {
                    ActiveManager.ApplyDrag(delta.x);
                }
                else if (currentDragDirection == DragDirection.Vertical)
                {
                    // 위/아래 스와이프 판단
                    if (delta.y > directionLockThreshold)
                    {
                        OnSwipeUp?.Invoke();    // 메뉴 -> 카테고리(상위계층 이동)
                        isDragging = false;
                    }
                    else if (delta.y < -directionLockThreshold)
                    {
                        OnSwipeDown?.Invoke();  // 카테고리 -> 메뉴(하위계층 이동)
                        isDragging = false;
                    }
                }

                lastMousePos = currentMousePos;
            });

        // 드래그 종료
        Observable.EveryUpdate()
            .Where(_ => Input.GetMouseButtonUp(0))
            .Subscribe(_ =>
            {
                isDragging = false;

                if (currentDragDirection == DragDirection.Horizontal)
                    ActiveManager.StartDecayAndSnap();

                currentDragDirection = DragDirection.None;
            });
    }
}
