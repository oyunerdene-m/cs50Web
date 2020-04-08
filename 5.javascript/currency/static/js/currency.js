document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#form").onsubmit = () => {

      const currency = document.querySelector("#currency");
      const request = new XMLHttpRequest();
      request.open("POST", "/convert");

      request.onload = () => {

        const data = JSON.parse(request.responseText);

        if(data.success){
          const content = `1 EUR equals to ${data['rate']} ${currency}`
          document.querySelector('#result').innerHTML = content;
        } else {
          document.querySelector('#result').innerHTML = "There was an error.";
        }
      }

      const data = new FormData();
      data.append("currency", currency);
      request.send(data);
      return false;
    };
});