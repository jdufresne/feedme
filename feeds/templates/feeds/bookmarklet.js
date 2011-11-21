	if(typeof jQuery=='undefined'){
		var jQ=document.createElement('script');
		jQ.type='text/javascript';
		jQ.onload=runthis;
		jQ.src='http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
		document.body.appendChild(jQ);
	}else{
		runthis();
	}
	function runthis(){
		var title=document.title;
		var url=document.URL;
		var comment=prompt('Share with comment:');
		$.post( '{{external_share_url}}',
				{
					title:title,
					comment:comment,
					url:url,
					user_id:'{{user_id}}',
				},
				function(data)
				{
					alert(data);
				}
		);
	}