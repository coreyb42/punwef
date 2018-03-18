import os
from subprocess import Popen, PIPE
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def get_phantom_driver(user_agent):
    desired_capabilities = dict(DesiredCapabilities.CHROME)
    desired_capabilities["phantomjs.page.settings.userAgent"] = user_agent
    driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
    return driver


def do_screen_capturing(url, screen_path, width, height):
    print("Capturing screen..")
    driver = get_phantom_driver(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/40.0.2214.115 Safari/537.36")
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(service_log_path='/var/log/phantomjs/ghostdriver.log')
    driver.set_script_timeout(5)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    source = driver.page_source
    driver.save_screenshot(screen_path)
    driver.quit()
    return source


def do_crop(params):
    print("Cropping captured image..")
    command = [
        'convert',
        params['screen_path'],
        '-crop', '%sx%s+0+0' % (params['width'], params['height']),
        params['crop_path']
    ]
    execute_command(' '.join(command))


def do_thumbnail(params):
    print("Generating thumbnail from cropped captured image..")
    command = [
        'convert',
        params['crop_path'],
        '-filter', 'Lanczos',
        '-thumbnail', '%sx%s' % (params['width'], params['height']),
        params['thumbnail_path']
    ]
    execute_command(' '.join(command))


def get_screen_shot(**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 1024))  # screen width to capture
    height = int(kwargs.get('height', 768))  # screen height to capture
    filename = kwargs.get('filename', 'screen.png')  # file name e.g. screen.png
    path = kwargs.get('path', ROOT)  # directory path to store screen

    crop = kwargs.get('crop', False)  # crop the captured screen
    crop_width = int(kwargs.get('crop_width', width))  # the width of crop screen
    crop_height = int(kwargs.get('crop_height', height))  # the height of crop screen
    crop_replace = kwargs.get('crop_replace', False)  # does crop image replace original screen capture?

    thumbnail = kwargs.get('thumbnail', False)  # generate thumbnail from screen, requires crop=True
    thumbnail_width = int(kwargs.get('thumbnail_width', width))  # the width of thumbnail
    thumbnail_height = int(kwargs.get('thumbnail_height', height))  # the height of thumbnail
    thumbnail_replace = kwargs.get('thumbnail_replace', False)  # does thumbnail image replace crop image?

    screen_path = abspath(path, filename)
    crop_path = thumbnail_path = screen_path

    if thumbnail and not crop:
        raise Exception('Thumbnail generation requires crop image, set crop=True')

    source = do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, 'crop_' + filename)
        params = {
            'width': crop_width, 'height': crop_height,
            'crop_path': crop_path, 'screen_path': screen_path}
        do_crop(params)

        if thumbnail:
            if not thumbnail_replace:
                thumbnail_path = abspath(path, 'thumbnail_' + filename)
            params = {
                'width': thumbnail_width, 'height': thumbnail_height,
                'thumbnail_path': thumbnail_path, 'crop_path': crop_path}
            do_thumbnail(params)
    return screen_path, crop_path, thumbnail_path, source
