from pepper.robot import Pepper

if __name__ == "__main__":
    # Press Pepper's chest button once and he will tell you his IP address
    ip_address = "10.68.110.200"
    port = 9559
    robot = Pepper(ip_address, port)
    robot.set_english_language()
    robot.set_volume(50)
    robot.say("Hello, is this working now?")
    robot.start_animation("Hey_1")
    robot.set_security_distance(0.2)
    robot.exploration_mode(4)
    robot.share_localhost()