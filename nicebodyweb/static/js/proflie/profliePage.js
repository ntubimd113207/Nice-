document.addEventListener("DOMContentLoaded", function () {
  //彈跳視窗 申請營養師身分
  let openapplynutritionist = document.getElementById('openapplynutritionist');
  let applynutritionist = document.getElementById('applynutritionist');
  let closeapplynutritionist = document.getElementById('closeapplynutritionist');

  openapplynutritionist.addEventListener("click", () => applynutritionist.showModal());
  closeapplynutritionist.addEventListener("click", () => applynutritionist.close());

  //編輯個資
  let changeButton = document.querySelector(".closesetting button:last-child");
  let inputs = [
    document.getElementById("name"),
    document.getElementById("birthday")
  ];
  let maleButton = document.getElementById("maleButton");
  let femaleButton = document.getElementById("femaleButton");
  let lockIcons = document.querySelectorAll(".fa-lock");

  function toggleEditMode(editMode) {
    inputs.forEach(input => {
      input.readOnly = !editMode;
      input.classList.toggle("disablededit", !editMode);
    });

    maleButton.classList.toggle("disablededit", !editMode);
    femaleButton.classList.toggle("disablededit", !editMode);

    lockIcons.forEach(icon => {
      icon.classList.toggle("fa-lock-open", editMode);
      icon.classList.toggle("fa-lock", !editMode);
    });
  }

  function updateButtonStyles(selectedButton) {
    if (selectedButton === maleButton) {
      selectedButton.style.border = "2px solid #297bcd";
      femaleButton.style.border = "#FF95CA 2px solid";
    } else {
      selectedButton.style.border = "2px solid #c22574";
      maleButton.style.border = "#84C1FF 2px solid";
    }
  }

  changeButton.addEventListener("click", function () {
    let inEditMode = changeButton.textContent === "變更個資";
    changeButton.textContent = inEditMode ? "儲存變更" : "變更個資";
    toggleEditMode(inEditMode);
  });

  toggleEditMode(false);

  maleButton.addEventListener("click", function () {
    if (changeButton.textContent === "變更個資") return;
    updateButtonStyles(maleButton);
  });

  femaleButton.addEventListener("click", function () {
    if (changeButton.textContent === "變更個資") return;
    updateButtonStyles(femaleButton);
  });
});