(function() {
    'use strict';

    const calendarEl = document.querySelector('.calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
        },
        initialDate: '2020-12-01',
        navLinks: true,
        businessHours: true,
        editable: true,
        locale: 'ja',
        events: [
          {
            title: 'カラオケ',
            start: '2020-12-03'
          },
          {
            title: 'ショッピング',
            start: '2020-12-03'
          },
          {
            title: '打ち合わせ',
            start: '2020-12-07T10:00:00',
            end: '2020-12-07T11:00:00'
          },
          {
            title: '打ち上げ',
            start: '2020-12-09T19:00:00'
          },
          {
              title: '会議',
              start: '2020-12-14T11:00:00',
              constraint: 'availableForMeeting'
            },
            {
              title: '打ち合わせ',
              start: '2020-12-14T13:00:00',
              end: '2020-12-14T13:30:00'
            },
            {
              title: '打ち合わせ',
              start: '2020-12-14T15:00:00',
              end: '2020-12-14T15:30:00'
            },
            {
              title: '打ち合わせ',
              start: '2020-12-14T16:30:00',
              end: '2020-12-14T18:00:00'
            },
            {
                title: 'セミナー',
                start: '2020-12-18T15:00:00',
                end: '2020-12-18T17:30:00'
            },
            {
                title: 'パーティー',
                start: '2020-12-23T20:00:00'
            },
            {
            title: '旅行',
            start: '2020-12-26',
            end: '2020-12-31'
          }
        ]
    });

    calendar.render();
}());