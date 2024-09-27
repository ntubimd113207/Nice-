//編輯個資
document.addEventListener("DOMContentLoaded", function () {
  let changeButton = document.getElementById("changeButton");
  let inputs = [
    document.getElementById("name"),
    document.getElementById("birthday")
  ];
  let maleButton = document.getElementById("maleButton");
  let femaleButton = document.getElementById("femaleButton");
  let lockIcons = document.querySelectorAll(".fa-lock");

  let originalData = {
    name: inputs[0].value,
    gender: maleButton.classList.contains("selected") ? "M" :
            femaleButton.classList.contains("selected") ? "F" : null,
    birthday: inputs[1].value === '' ? null : inputs[1].value
  };  

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
      maleButton.classList.add('selected');
      femaleButton.classList.remove('selected');
    } else {
      selectedButton.style.border = "2px solid #c22574";
      maleButton.style.border = "#84C1FF 2px solid";
      femaleButton.classList.add('selected');
      maleButton.classList.remove('selected');
    }
  }

  changeButton.addEventListener("click", function () {
    console.log(changeButton.textContent);
    if (changeButton.textContent === "儲存變更") {
      inEditMode = changeButton.textContent === "變更個資";
      // Check for changes
      let currentData = {
        name: inputs[0].value,
        gender: maleButton.classList.contains("selected") ? "M" :
            femaleButton.classList.contains("selected") ? "F" : null,
        birthday: inputs[1].value === '' ? null : inputs[1].value
      };

      console.log(currentData);
      console.log(originalData);
      
      if (currentData.name !== originalData.name ||
          currentData.gender !== originalData.gender ||
          currentData.birthday !== originalData.birthday) {
          document.getElementById("messageText").textContent = currentData.name;

          if (currentData.name === "") {
            alert("請輸入姓名");
            return;
          }

          if (/\s/.test(currentData.name)) {
            alert("姓名不能包含空格");
            return;
          }
            
          $.ajax({
            type: 'POST',
            url: '/profile/updateProfile',
            data: {
              name: currentData.name,
              gender: currentData.gender,
              birthday: currentData.birthday
            },
            success: function(response) {
              console.log(response);
              originalData = currentData;
            },
            error: function(xhr, status, error) {
              console.error(error);
              alert('出現錯誤，請稍後再試！');
            }
          });
      }
    }
    else {
      inEditMode = changeButton.textContent === "變更個資";
    }
    changeButton.textContent = inEditMode ? "儲存變更" : "變更個資";
    toggleEditMode(inEditMode);
  });

  toggleEditMode(false);

  maleButton.addEventListener("click", function () {
    updateButtonStyles(maleButton);
  });

  femaleButton.addEventListener("click", function () {
    updateButtonStyles(femaleButton);
  });
});
  