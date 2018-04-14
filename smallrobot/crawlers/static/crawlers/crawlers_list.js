$('.runCrawlerForm').submit(function (event) {
  event.preventDefault();
  var form=$(this);
  $.get( form.attr('action'), form.serialize(), function( data ) {
    console.log( data );
    alert( "Load was performed." );
  });
  return false;
})