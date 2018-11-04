function changetext()
{
  document.getElementById("heading").innerHTML = response;
}
/*
function ajaxer()
{
  console.log('im being called');
  $.ajax({
         url: '/main/chat',
         data: ,
         type: 'POST',
         success: function(response) {
           document.getElementById("heading").innerHTML = response;
         },
         error: function(error) {
             console.log(error);
         }
     });
}


var sb = new SendBird({appId: "A698EF3E-71F1-4E3A-B762-58A53E356846"});

sb.connect("testbot1", "ff6c17787c277e2deaa98797a240487199510a1a", function(user, error)
  {
    if (error)
    {
      return;
    }
  }
);

sb.OpenChannel.createChannel(function(openChannel, error)
  {
    if (error)
      {
        return;
      }
  }
);

sb.OpenChannel.getChannel("frogsfrogsfrogs", function(openChannel, error)
  {
    if (error)
    {
      return;
    }

    openChannel.enter(function(response, error)
      {
        if (error)
        {
          return;
        }
      })

    openChannel.sendUserMessage("hello!", DATA, USER_MESSAGE, function(message, error)
      {
        if (error)
        {
          return;
        }
      })
    }
);*/
