templates =
  comment: '/static/comment.tmpl'
  edit_comment: '/static/edit-comment.tmpl'
  delete_comment: '/static/delete-comment.tmpl'
  

$('body').on 'click', '.alert:not(.modal)', () ->
  $(this).fadeOut()

$('body').on 'click', '.edit', (e) ->
  controls = $(this).parent()
  comment = controls.parent()
  username = comment.find '.anonymous'
  content = comment.find '.content'

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
  controls.append actions

  save_btn.on 'click', save_edit
  cancel_btn.on 'click', hide_form
  e.preventDefault()

hide_form = (e) ->
  comment = $(this).parent().parent().parent()
  comment.find('input, textarea, .comment-actions').remove()
  comment.find('.anonymous, .content').show()
  e?.preventDefault()

save_edit = (e) ->
  comment = $(this).parent().parent().parent()
  url = comment.find('.edit').attr('href')
  new_username = $('input').val()
  new_content = $('textarea').val()
  token = $(document.body).data('token')

  $(this).attr('disabled', '')
  e.preventDefault()
  return

  $.ajax
    type: 'POST'
    url: url
    data: "username=#{new_username}&content=#{new_content}"+
      "&token=#{token}"
    dataType: 'json'
    success: (data) =>
      if data.status is 'success'
        comment.find('.anonymous').text(new_username) if new_username
        comment.find('.content').text(new_content)
        hide_form.call(this)
      else
        message data
        $(this).removeAttr 'disabled'

      $(document.body).data('token', data.token)
      console.log 'set token', data.token
    error: (data) =>
      message status: 'error', message: "#{data.status}: #{data.statusText}"
      $(this).removeAttr 'disabled'

$('body').on 'click', '.delete', (e) ->
  url = $(this).attr('href')
  token = $(document.body).data('token')
  comment = $(this).parent().parent().parent().parent()
  modal = message(status: 'danger', message: '')
  modal.html('<strong>Are you sure</strong> you want to delete this comment?')

  delete_btn = $('<button class="btn btn-danger btn-small">')
    .text('Yes, delete this comment')
  cancel_btn = $('<button class="btn btn-small">').text('Cancel')
  modal.append delete_btn
  modal.append cancel_btn

  delete_btn.on 'click', ->
    modal.modal('hide')
    $.ajax
      type: 'POST'
      url: url
      data: "token=#{token}&action=delete"
      dataType: 'json'
      success: (data) =>
        if data.status is 'success'
          comment.fadeOut()
        else
          message(data)

        $(document.body).data('token', data.token)
      error: (data) =>
        message status: 'error', message: "#{data.status}: #{data.statusText}"

  cancel_btn.on 'click', ->
    modal.modal('hide')

  e.preventDefault()

$('#add-comment').on 'submit', 'form', (e) ->
  url = $(this).attr('action')
  token = $(document.body).data('token')
  $(this).find('[name="token"]').val(token)

  $.ajax
    type: 'POST'
    url: url
    data: $(this).serialize()
    dataType: 'json'
    success: (data) =>
      if data.status is 'success'
        alert 'all went well'
      else
        message(data)

      $(document.body).data('token', data.token)
    error: (data) =>
      message status: 'error', message: "#{data.status}: #{data.statusText}"
  e.preventDefault()

message = (data) ->
  modal = $("<div class=\"modal alert alert-#{data.status}\">")
  modal.text(data.message)
  $(document.body).append(modal)
  modal.modal()
