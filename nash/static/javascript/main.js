if (location.hash == '#good') {
    document.getElementById('result').innerHTML = '<div class="good-result">File uploaded successfully.</div>';
    setTimeout(function() {
      document.getElementById('result').remove();
    }, 2000);
  } else if (location.hash == '#error') {
    document.getElementById('result').innerHTML = '<div class="error-result">Error while loading the file.</div>';
  }


  (function($) {
    'use strict';
    $(document).on('show.bs.tab', '.nav-tabs-responsive [data-toggle="tab"]', function(e) {
      var $target = $(e.target);
      var $tabs = $target.closest('.nav-tabs-responsive');
      var $current = $target.closest('li');
      var $parent = $current.closest('li.dropdown');
      $current = $parent.length > 0 ? $parent : $current;
      var $next = $current.next();
      var $prev = $current.prev();
      var updateDropdownMenu = function($el, position){
        $el
          .find('.dropdown-menu')
          .removeClass('pull-xs-left pull-xs-center pull-xs-right')
          .addClass( 'pull-xs-' + position );
      };
  
      $tabs.find('>li').removeClass('next prev');
      $prev.addClass('prev');
      $next.addClass('next');
      
      updateDropdownMenu( $prev, 'left' );
      updateDropdownMenu( $current, 'center' );
      updateDropdownMenu( $next, 'right' );
    });
  
  })(jQuery);