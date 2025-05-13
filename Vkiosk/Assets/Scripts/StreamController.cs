using UnityEngine;

public class StreamController : MonoBehaviour
{
    public MenuInputHandler menuInputHandler;
    public MenuSpinningManager categoryMenuManager; // ī�װ���
    public MenuSpinningManager itemMenuManager;     // �޴�(������)��

    private MenuState currentState = MenuState.Category;

    private void Start()
    {
        // �Է� �ڵ鷯�� �ݹ� ���
        menuInputHandler.OnSwipeDown = SwitchToMenuView;
        menuInputHandler.OnSwipeUp = SwitchToCategoryView;

        categoryMenuManager.gameObject.SetActive(true);
        itemMenuManager.gameObject.SetActive(false);
    }

    private void SwitchToMenuView()
    { 
        if (currentState != MenuState.Category) return;

        currentState = MenuState.Menu;
        menuInputHandler.SetState(currentState);
        categoryMenuManager.gameObject.SetActive(false);
        itemMenuManager.gameObject.SetActive(true);
    }

    private void SwitchToCategoryView()
    {
        if (currentState != MenuState.Menu) return;

        currentState = MenuState.Category;
        menuInputHandler.SetState(currentState);
        itemMenuManager.gameObject.SetActive(false);
        categoryMenuManager.gameObject.SetActive(true);
    }
}
