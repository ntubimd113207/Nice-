let messageText = "{{data}}";
window.onload = function () {
    // Navbar
    renderNav();

    // 變數
    let tags = [];

    const continueBtn = document.getElementById('continue-btn');

    const inputField = document.getElementById('tag-ip');

    const savedValue = sessionStorage.getItem('tagInputValue');
    
    // 检查输入框中是否有文本，并根据情况更新按钮状态和样式
    function checkInput() {
        if (inputField.value.trim() !== '' || tags.length > 0) {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n2');
            
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    }

    continueBtn.addEventListener('click', function () {
        const tagInput = document.getElementById('tag-ip');
        sessionStorage.setItem('tagInputValue', tagInput.value);
        sessionStorage.removeItem('tagInputValue2');
        sessionStorage.removeItem('selectedTag1Count');
    });

    inputField.addEventListener('input', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue !== '') {
            continueBtn.classList.add('button-brwon');
            continueBtn.setAttribute('href', '/question/question_n2');
        } else {
            continueBtn.classList.remove('button-brwon');
            continueBtn.removeAttribute('href');
        }
    });

    continueBtn.addEventListener('click', function() {
        const inputValue = inputField.value.trim(); // 獲取去除兩端空格的輸入值
        if (inputValue === '') {
            alert('請輸入內容');
        } 
    });

    document.querySelectorAll('.diet-tag a').forEach(function(tag) {
      tag.addEventListener('click', function() {
          // Toggle 'select' class for the clicked <a> element
          if (this.classList.contains('select')) {
              this.classList.remove('select');
          } else {
              this.classList.add('select');
          }

          // Get all selected tags' text
          var selectedTexts = [];
          document.querySelectorAll('.diet-tag a.select h6').forEach(function(selectedTag) {
              selectedTexts.push(selectedTag.textContent);
          });

          // Set the joined selected texts to the input with id 'tag-ip'
          document.getElementById('tag-ip').value = selectedTexts.join('、');

          checkInput();
      });
  });

  if (savedValue !== null) {
      inputField.value = savedValue;
      checkInput();
      const selectedTags = savedValue.split('、').map(tag => tag.trim());
      selectedTags.forEach(tag => {
          document.querySelectorAll('.diet-tag a').forEach(function(tagElement) {
              console.log(tagElement.querySelector('h6').textContent);
              if (tagElement.querySelector('h6').textContent === tag) {
                  tagElement.classList.add('select');
              }
          });
      });
  }

    
};