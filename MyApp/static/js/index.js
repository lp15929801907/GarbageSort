$(function() {
	$('.d-firstNav').click(function(e) {
		console.log("111");
		dropSwift($(this), '.d-firstDrop');	   
		e.stopPropagation();
	});
	$('.d-secondNav').click(function(e) {
		dropSwift($(this), '.d-secondDrop');
		e.stopPropagation();
	});
	
	
	
	/**
	 * @param dom   点击的当前元素
	 * @param drop  下一级菜单
	 */
	function dropSwift(dom, drop) {
		//点击当前元素，收起或者伸展下一级菜单
		
		
		dom.next().slideToggle();
		
		//设置旋转效果
		
		//1.将所有的元素都至为初始的状态		
		dom.parent().siblings().find('.fa-caret-right').removeClass('iconRotate');
		
		//2.点击该层，将其他显示的下滑层隐藏		
		dom.parent().siblings().find(drop).slideUp();
		
		var iconChevron = dom.find('.fa-caret-right');
		if(iconChevron.hasClass('iconRotate')) {
			iconChevron.removeClass('iconRotate');
		} else {
			iconChevron.addClass('iconRotate');
		}
	}
})