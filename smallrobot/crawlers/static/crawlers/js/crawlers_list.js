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
  var loading = $(`.loading-result.result-${resultId}`);
  var submitButton = $(`.crawler-run-button.result-${resultId}`);
  var errorInfo = submitButton.closest('.runCrawlerForm').find('.error-info')
  const endLoad = ()=>{
    loading.removeClass(`result-${resultId}`);
    loading.addClass('d-none');
    submitButton.removeClass(`result-${resultId} d-none`);
  };
  $.fileDownload(`/crawlers/result?resultid=${resultId}`, {
    successCallback: function (url) {
      endLoad();
    },
    failCallback: function (responseHtml, url) {
      if (responseHtml === "loading") {
        setTimeout(()=>checkForResults(resultId),35000);
        return false
      }else{
        errorInfo.fadeIn()
        endLoad();
        console.log('ERROR:',responseHtml);
      }
    }
  });
}

$(document).on('submit', '.runCrawlerForm', function(event){
  event.preventDefault();
  var form=$(this);
  form.find('.error-info').fadeOut()
  var rl=form.find('.loading-result');
  var submitButton = form.find('.crawler-run-button')
  rl.removeClass('d-none');
  submitButton.addClass('d-none');
  $.get( form.attr('action'), form.serialize(), function( resultId ) {
    console.log( resultId );
    rl.addClass('result-'+resultId);
    submitButton.addClass('result-'+resultId);
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
  var profile = $(this).closest('.profile')
  profile.addClass('d-none deleted-profile')
})