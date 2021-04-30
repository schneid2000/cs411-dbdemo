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

    //Might do nothing I have no idea
    $('#login-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        const modal = $(this)
        if (taskID === 'loginuser') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Task ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-login').click(function () {
        netid = $('#login-modal').find('.login-form-netid').val()
        pw = $('#login-modal').find('.login-form-pw').val()
        major = $('#login-modal').find('.login-form-mj').val()
        console.log(netid)
        console.log(pw)
        console.log(major)
        hashed_pw = sha3_256(pw)
        console.log(hashed_pw)
        $.ajax({
            type: 'POST',
            url: '/login',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'netid':netid,
                'pw':hashed_pw,
                'mj':major
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

    $('#submit-gen-schedule').click(function () {
        console.log("Button clicked!")
        schedulename = $('.gen-form-schedule').val()
        console.log(schedulename)
        $.ajax({
            type: 'POST',
            url: '/new_schedule',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'sname':schedulename
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

    $('#select-major-req').click(function (event) {
        console.log("Select major req button")
        reqid = $(this).data('id')
        console.log(reqid)
        $.ajax({
            type: 'POST',
            url: '/gen_schedule',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'req':reqid
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

    $('#submit-logout').click(function () {
        $.ajax({
            type: 'POST',
            url: '/logout',
            contentType: 'application/json;charset=UTF-8',
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });


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