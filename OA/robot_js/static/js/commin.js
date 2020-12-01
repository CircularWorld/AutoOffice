
function regist(){
		var user_talk = $('.talk_word').val();
		console.log(user_talk);
            $.ajax({
			url:'http://127.0.0.1:8000/robot/tallk',
			type:'POST',
			dataType:'json',
			data:JSON.stringify(user_talk),
			contentType:'application/json',
			success:function(res){
				if(res.code == 200){
					alert('注册成功！');
					// 将后端返回的数据保存到浏览器的本地存储
					window.localStorage.setItem('dnblog_token',res.data.token);
					window.localStorage.setItem('dnblog_user',res.username);
				}else{
					alert(res.error)
				}
			}
		})
		}