var sb = new SendBird({appId: APP_ID});

sb.connect(USER_ID, function(user, error) {if (error){return;}});

sb.OpenChannel.createChannel(function(openChannel, error)
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
  }
);

opeChannel.sendUserMessage(MESSAGE, DATA, CUSTOM_TYPE, function(message, error)
  {
    if (error)
    {
      return;
    }
  });


function changetext()
{
  document.getElementById("heading").innerHTML = "idid";
}
