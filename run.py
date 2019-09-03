from Api.api import app
from Schedule.schedule import Schedule


def main():
    s = Schedule()
    s.run()  # 启动代理池
    app.run()  # 启动代理池对外API接口


if __name__ == '__main__':
    main()
