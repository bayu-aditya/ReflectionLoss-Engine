def CustomException(e):
  try:
    error = e.args[0]
    code = e.args[1]
    return {
      "message": error}, code

  except:
    return {"error": str(e)}, 500