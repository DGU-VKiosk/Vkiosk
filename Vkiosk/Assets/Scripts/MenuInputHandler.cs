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
        // �巡�� ����
        Observable.EveryUpdate()
            .Where(_ => Input.GetMouseButtonDown(0))
            .Subscribe(_ =>
            {
                isDragging = true;
                lastMousePos = Input.mousePosition;
                currentDragDirection = DragDirection.None;
            });

        // �巡�� ��
        Observable.EveryUpdate()
            .Where(_ => isDragging)
            .Subscribe(_ =>
            {
                Vector2 currentMousePos = Input.mousePosition;
                Vector2 delta = currentMousePos - lastMousePos;

                // ���� �Ǵ�
                if (currentDragDirection == DragDirection.None)
                {
                    if (delta.magnitude > directionLockThreshold)
                    {
                        currentDragDirection = Mathf.Abs(delta.x) > Mathf.Abs(delta.y)
                            ? DragDirection.Horizontal
                            : DragDirection.Vertical;
                    }
                }

                // ���⿡ ���� ����
                if (currentDragDirection == DragDirection.Horizontal)
                {
                    ActiveManager.ApplyDrag(delta.x);
                }
                else if (currentDragDirection == DragDirection.Vertical)
                {
                    // ��/�Ʒ� �������� �Ǵ�
                    if (delta.y > directionLockThreshold)
                    {
                        OnSwipeUp?.Invoke();    // �޴� -> ī�װ�(�������� �̵�)
                        isDragging = false;
                    }
                    else if (delta.y < -directionLockThreshold)
                    {
                        OnSwipeDown?.Invoke();  // ī�װ� -> �޴�(�������� �̵�)
                        isDragging = false;
                    }
                }

                lastMousePos = currentMousePos;
            });

        // �巡�� ����
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
