odoo.define('crm_logout.crm_logout_systray', function (require) {
   "use strict";
   var core = require('web.core');
   var QWeb = core.qweb;
   var Widget = require('web.Widget');
   var SystrayMenu = require('web.SystrayMenu');
   var rpc = require('web.rpc');
   var session = require('web.session');
    var milisec = 0;
    var x;
    var sec = 0;
    var min = 0;
    var hour = 0;
    var miliSecOut = 0;
    var secOut = 0;
    var minOut = 0;
    var hourOut = 0;
    var fields = ['idle_time_limit','next_question_limit']
    var rpc = require('web.rpc');
    var domain =[];

   var Weather = Widget.extend({
       template: 'crm_logout_systray',
       init: function(){
            var self = this;
//            console.log(self, 'self')
                var limit = 10
                var new_interval = limit * 60000
                var idleInterval = setTimeout(start, 30000);
                function start() {
                    x = setInterval(timer, 10);
                }
                function timer() {
                  miliSecOut = checkTime(milisec);
                  secOut = checkTime(sec);
                  minOut = checkTime(min);
                  hourOut = checkTime(hour);
                  milisec = ++milisec;
                  if (milisec === 100) {
                    milisec = 0;
                    sec = ++sec;
                  }
                  if (sec == 60) {
                    min = ++min;
                    sec = 0;
                  }
                  if (min == 60) {
                    min = 0;
                    hour = ++hour;
                  }
                  jQuery('#min').html(secOut);
                  jQuery('#sec').html(minOut);
                }
                function checkTime(i) {
                  if (i < 10) {
                    i = "0" + i;
//                    console.log(i,'i')
                  }
                  return i;
                }
                var nextInterval = setInterval(nextTimerIncrement, 300000);
                function nextTimerIncrement() {
                    window.location.href = "/web/session/logout";
                }
              $('body').mousemove(function (e) {
                  milisec = 0;
                  sec = 0;
                  min = 0
                  hour = 0;
                  idleInterval = 0;
                  clearTimeout(idleInterval);
              });

              $('body').keypress(function (e) {
                  milisec = 0;
                  sec = 0;
                  min = 0
                  hour = 0;
                  jQuery('#min').html('00');
                  jQuery('#sec').html('00');
                  clearTimeout(idleInterval);
              });
              $('body').click(function() {
                  milisec = 0;
                  sec = 0;
                  min = 0
                  hour = 0;
                  jQuery('#min').html('00');
                  jQuery('#sec').html('00');
                  clearTimeout(idleInterval);
              });

       }
   });
   SystrayMenu.Items.push(Weather);
   return Weather;
});
