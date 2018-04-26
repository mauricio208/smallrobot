function lastResult(id, dateTime, url){
  return `<div class="list-group-item" id="result-${id}">
  <div class="col text-muted" style="text-align:center;">
  ${dateTime}
  </div>
  <div class="col" style="text-align:center;">
  <a class="btn btn-success" href="${url}" role="button"><i class="fas fa-download" data-fa-transform="grow-2"></i></a>
  </div>
  </div>`;
}

function checkForResults(resultId) {
  $.fileDownload(`/crawlers/result?resultid=${resultId}`, {
    successCallback: function (url) {
      console.log('sucesscallback');
      var rl=form.find('.loading-result');
      rl.addClass('d-none');
    },
    failCallback: function (responseHtml, url) {
      if (responseHtml === "loading") {
        setTimeout(()=>checkForResults(resultId),35000);
        return false
      }else{
        alert('File download failed!');
      }
    }
  });
  // $.getJSON('lastresult', {'crawlerid':crawlerId},function (data) {
  //   var cr=$('#crawler-'+crawlerId).find('.crawler-results');
  //   var rl=cr.find('.loading-result');
    
  //   if (rl.next('.list-group-item').attr('id') === "result-"+data.id){
  //     setTimeout(()=>checkForResults(crawlerId),30000);
  //   }else{
  //     rl.addClass('d-none');
  //     rl.after(lastResult(data.id, data.date_time, data.url))
  //   }
  // })
}

$('.runCrawlerForm').submit(function (event) {
  event.preventDefault();
  var form=$(this);
  var rl=form.find('.loading-result');
  rl.removeClass('d-none');
  $.get( form.attr('action'), form.serialize(), function( resultId ) {
    console.log( resultId );
    rl.addClass('result-'+resultId);
    setTimeout(()=>checkForResults(resultId),35000);
  });
  // $.fileDownload(form.attr('action')+'?'+form.serialize(), {
  //   prepareCallback: function (url) {
  //     console.log('sucesscallback');
  //     var rl=form.find('.loading-result');
  //     rl.addClass('d-none');
  //   },
  //   failCallback: function (responseHtml, url) {
  //     alert('File download failed!');
  //   }
  // });
  return false;
})

$('.addProfile').click(function(event) {
  var el = $(this).parent('.row')
  var newProfile = el.find('.template-profile').clone();
  newProfile.addClass('profile');
  newProfile.removeClass('d-none template-profile')
  el.before(newProfile);
})

$(document).on('click', '.removeProfile', function(event){
  var profile = $(this).parent('.profile')
  profile.addClass('d-none deleted-profile')
})