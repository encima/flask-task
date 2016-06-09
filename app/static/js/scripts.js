$(document).ready( function() {

    $('tr').on('click', function(e){ 
        var self = this;
        $.ajax({
            url:"/do",
            method:"POST",
            data:{"id":this.getAttribute('data-id')},
            success:function(data) {
                console.log(data);
				//todo remove table with dynamic key
				if(data['project'] in data['table']) {
					$(self).parent().parent().html(data['table'][data['project']])
				} else {
					$(self).closest('div').remove();
				}
            }
        });
    }); 
});
