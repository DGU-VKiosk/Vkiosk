using UnityEngine;

public class StreamController : MonoBehaviour
{
    public MenuInputHandler menuInputHandler;
    public MenuSpinningManager categoryMenuManager; // 카테고리용
    public MenuSpinningManager itemMenuManager;     // 메뉴(아이템)용

    private MenuState currentState = MenuState.Category;

    private void Start()
    {
        // 입력 핸들러에 콜백 등록
        menuInputHandler.OnSwipeDown = SwitchToMenuView;
        menuInputHandler.OnSwipeUp = SwitchToCategoryView;

        categoryMenuManager.gameObject.SetActive(true);
        itemMenuManager.gameObject.SetActive(false);
    }

    private void SwitchToMenuView()
    { 
        if (currentState != MenuState.Category) return;

        currentState = MenuState.Menu;
        categoryMenuManager.gameObject.SetActive(false);
        itemMenuManager.gameObject.SetActive(true);
    }

    private void SwitchToCategoryView()
    {
        if (currentState != MenuState.Menu) return;

        currentState = MenuState.Category;
        itemMenuManager.gameObject.SetActive(false);
        categoryMenuManager.gameObject.SetActive(true);
    }
}
