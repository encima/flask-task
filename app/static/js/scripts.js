$(document).ready( function() {
    console.log('ready');

    //todo add click listener for table
    
    var rows = document.getElementsByTagName('tr')
    
    for(var i = 0; i < rows.length; i++) {
        rows[i].onclick = function(e) {
            console.log(this.getAttribute('data-id'));
        }
    }
    // $('tr').click(function(e) {
    //     console.log($(this).data('id'));
    //     $.post()
    // });
});
