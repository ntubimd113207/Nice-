document.addEventListener('DOMContentLoaded', function () {
    const lockIcons = document.querySelectorAll('.lock-icon');
    const closeButton = document.querySelector('.closesetting .button');
    let unlockedFields = [];

    // 初始化時禁用所有可輸入的欄位
    function disableAllInputs() {
        const inputs = document.querySelectorAll('.settings input');
        inputs.forEach(input => {
            input.disabled = true;
        });
    }

    disableAllInputs();

    // 點擊鎖圖標時解鎖對應的輸入欄位
    lockIcons.forEach(icon => {
        icon.addEventListener('click', function () {
            const parentDiv = icon.closest('div');
            const inputField = parentDiv.querySelector('input');
            if (inputField) {
                inputField.disabled = !inputField.disabled; // 切換輸入欄位的禁用狀態
                if (!inputField.disabled && !unlockedFields.includes(inputField)) {
                    unlockedFields.push(inputField);
                } else if (inputField.disabled && unlockedFields.includes(inputField)) {
                    const index = unlockedFields.indexOf(inputField);
                    unlockedFields.splice(index, 1);
                }
            }
        });
    });

    // 點擊 "變更個資" 按鈕後鎖定所有已解鎖的欄位
    closeButton.addEventListener('click', function () {
        unlockedFields.forEach(field => {
            field.disabled = true;
        });
        unlockedFields = [];
    });
});
