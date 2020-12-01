var BASE_URL = '../static/images/';//规定当前文件中的图片的地址

// 轮播图
$(function(){
    //  alert('外部JS加载完成')//jquery 加载成功
     console.log(faderData)//外部数据加载成功
    //根据从faderData中获取的数据拼接字符串
    // <li class="slide">...</li><li></li><li></li>
    // 再拼接上<div class="fader_controls"></div>中的元素
    // 最后将字符串放入页面元素ul id='fader'

    var html = '';
    $.each(faderData,function(i,obj){
        html += '<li class="slide">'
        html += '<a href="#">'
        html += `<img src="${BASE_URL+obj.img_url}" alt=""></a>`   
        html += `<div class="imginfo">${obj.img_info}</div>`    
        html +=  '</li>'
    })
    html += '<li class="fader_controls">'
    html += '<div class="page prev" data-target="prev">&lsaquo;</div>'
    html += '<div class="page next" data-target="next">&rsaquo;</div>'
    html += '<ul class="pager_list">'
    html += '</ul></li>'
    // easyFader()是由easyfader.min.js提供的功能
    // 实现图片轮播效果
    $('#fader').html(html).easyFader({
        slideDur:4000,/*切换图片的时间间隔 ms*/ 
        fadeDur:1000,/*过渡的事件 ms*/
    })
    
})
