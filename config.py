from configparser import ConfigParser


def parse_xy(xy):
    x, y = xy.split(',')
    return int(x), int(y)


def merge_xy(x, y):
    return ','.join([str(x),str(y)])


class ROIConfiguration:
    def __init__(self, configfile_path):
        self.configfile_path = configfile_path
        self.bl_x = 0
        self.bl_y = 0
        self.br_x = 0
        self.br_y = 0
        self.tr_x = 0
        self.tr_y = 0
        self.tl_x = 0
        self.tl_y = 0
        self.width = 0
        self.depth = 0
        self.video_source = 0

    def initialize(self):
        config = ConfigParser()
        config.read(self.configfile_path)
        self.bl_x, self.bl_y = parse_xy(config['ROI']['bottomleft'])
        self.br_x, self.br_y = parse_xy(config['ROI']['bottomright'])
        self.tl_x, self.tl_y = parse_xy(config['ROI']['topleft'])
        self.tr_x, self.tr_y = parse_xy(config['ROI']['topright'])
        self.width = int(config['DIMENSION']['width'])
        self.depth = int(config['DIMENSION']['depth'])
        self.video_source = config['VIDEO']['source']

    def save(self):
        config = ConfigParser()
        config['ROI'] = {}
        config['ROI']['bottomleft'] = merge_xy(self.bl_x, self.bl_y)
        config['ROI']['bottomright'] = merge_xy(self.br_x, self.br_y)
        config['ROI']['topleft'] = merge_xy(self.tl_x, self.tl_y)
        config['ROI']['topright'] = merge_xy(self.tr_x, self.tr_y)
        config['DIMENSION'] = {}
        config['DIMENSION']['width'] = str(self.width)
        config['DIMENSION']['depth'] = str(self.depth)
        config['VIDEO'] = {}
        config['VIDEO']['source'] = self.video_source
        with open(self.configfile_path, 'w') as configfile:
            config.write(configfile)

