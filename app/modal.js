$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)

        // if (taskID == 'New Task') {
        //     modal.find('.modal-title').text(taskID)
        //     modal.find('#netid-modal-body').show()
        //     $('#task-form-display').removeAttr('taskID')
        // } else {
        //     modal.find('.modal-title').text('Edit Task ' + taskID)
        //     modal.find('#netid-modal-body').hide()
        //     $('#task-form-display').attr('taskID', taskID)
        // }

        // if (content) {
        //     modal.find('.sched-name').val(content);
        // } else {
        //     modal.find('.sched-name').val('');
        // }
    })


    $("#submit-search").click(function () {
        // e.preventDefault();
        // Get input field values
        // const tID = $('#task-form-display').attr('taskID');
        console.log($('#key').find('.search').val())
        $.ajax({
            type: 'POST',
            url: '/search',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': $('#key').find('.search').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $("#fliter-subject").click(function () {
        // e.preventDefault();
        // Get input field values
        // const tID = $('#task-form-display').attr('taskID');
        console.log($('#key').find('.filter-subject').val())
        $.ajax({
            type: 'POST',
            url: '/filter-subject',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': $('#key').find('.filter-subject').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $("#fliter-title").click(function () {
        // e.preventDefault();
        // Get input field values
        // const tID = $('#task-form-display').attr('taskID');
        console.log($('#key').find('.filter-title').val())
        $.ajax({
            type: 'POST',
            url: '/filter-subject',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': $('#key').find('.filter-title').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $("#crn-choice").click(function () {
        // e.preventDefault();
        // Get input field values
        // const tID = $('#task-form-display').attr('taskID');
        console.log($('#key').find('.crn-choice').val())
        $.ajax({
            type: 'POST',
            url: '/filter-subject',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'keyword': $('#key').find('.crn-choice').val(),
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


    $('#submit-task').click(function () {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.sched-name').val())
        $.ajax({
            type: 'POST',
            url: tID ? '/edit/' + tID : '/create',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'ScheduleName': $('#task-modal').find('.sched-name').val(),
                'Student': $('#task-modal').find('.student-netid').val(),
                'IsFavorite': $('#task-modal').find('.is-fav').val(),
                'IsShared': 0,
                'TotalCredits': 0
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#adv-q').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/AdvQ',
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('.remove').click(function () {
        const remove = $(this)
        $.ajax({
            type: 'POST',
            url: '/delete/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


});