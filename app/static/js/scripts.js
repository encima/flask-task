$(document).ready( function() {

    $('tr').on('click', function(e){ 
        var self = this;
		doTask(self);
    }); 

	function doTask(self) {
        $.ajax({
            url:"/do",
            method:"POST",
            data:{"id":self.getAttribute('data-id')},
            success:function(data) {
                console.log(data);
				//todo remove table with dynamic key
				if(data['project'] in data['table']) {
					$(self).parent().parent().html(data['table'][data['project']])
				} else {
					$(self).closest('div').remove();
				}
				$('tr').on('click', function(e){ 
					var self = this;
					doTask(self);
				}); 
            }
        });
	}
});
