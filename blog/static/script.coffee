$('body').on 'click', '.edit', (e) ->
  comment = $(this).parent().parent()
  username = comment.find '.anonymous'
  content = comment.children '.content'

  username.hide()
  content.hide()

  new_username = $('<input type="text">').val username.text().trim()
  new_content = $('<textarea class="span11">').val content.text().trim()

  actions = $('<div class="comment-actions">')
  save_btn = $('<button class="btn btn-primary">').text('Save')
  cancel_btn = $('<button class="btn">').text('Cancel')
  actions.append save_btn
  actions.append cancel_btn

  username.after new_username
  content.after new_content
  new_content.after actions

  save_btn.on 'click', save_edit
  cancel_btn.on 'click', hide_form
  e.preventDefault()

hide_form = (e) ->
  comment = $(this).parent().parent()
  comment.find('input, textarea, .comment-actions').remove()
  comment.find('.anonymous, .content').show()
  e?.preventDefault()

save_edit = (e) ->
  comment = $(this).parent().parent()
  url = comment.find('.edit').attr('href')
  new_username = $('input').val()
  new_content = $('textarea').val()
  token = $(document.body).data('token')

  $(this).attr('disabled', 'disabled')
  e.preventDefault()

  $.ajax
    type: 'POST'
    url: url
    data: "?username=#{new_username}&content=#{new_content}"+
      "&token=#{token}"
    dataType: 'json'
    success: (data) =>
      if data.status is 'success'
        comment.find('.anonymous').text(new_username) if new_username
        comment.find('.content').text(new_content)
        $(document.body).data('token', data.token)
        hide_form.call(this)
      else
        alert data.message
        $(this).removeAttr 'disabled'
    error: (data) =>
      alert "#{data.status}: #{data.statusText}"
      $(this).removeAttr 'disabled'
