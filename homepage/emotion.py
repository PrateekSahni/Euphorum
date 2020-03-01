from paralleldots import set_api_key, get_api_key, emotion

def get_emotion(line):

    set_api_key("VsjsIMn9VEkVhEoUrwa7EnNF6o6w0xvOeLwsoVeuyhk")
    #get_api_key()
    # line=str('mytextbox')
    result=emotion(line)
    #print("Emotions : ",result['probabilities'])
    #print("Final emotion : ",result['emotion'])
    return result['emotion']['emotion']
