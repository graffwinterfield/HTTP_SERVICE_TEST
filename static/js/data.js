<script>


$(document).ready(function () {

    var loading = false;
    var page = {{ page }};
    var data = "{{ data }}";
    var filename = "{{ filename }}";
    function loadData(pageNumber) {


    console.log('http://127.0.0.1:5000/details/' + filename + '?page=' + page + '&' +  Math.random());

    console.log('?page=' + pageNumber);

        $.ajax({
          url: '/details/' + filename + '?page=' + page + '&' +  Math.random(),
          method: 'GET',
          dataType: 'html',
          success: function(response) {
          console.log(data);
              // Обработка полученных данных и добавление их на страницу
            $("#data-container").html(data);

              page = pageNumber + 1;

          },
          error: function(xhr, status, error){
         var errorMessage = xhr.status + ': ' + xhr.statusText

         console.log(errorMessage);}
        });
        page = pageNumber + 1;

    }




    // Подписка на событие клика на кнопке

    $("#pagination-next-btn").click(function() {
        loadData(page);
    });
  });
</script>