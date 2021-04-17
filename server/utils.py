__all__ = ['check_config_json', 'get_local_json']

import json


def load_config_json():
    with open('config.json', 'r', encoding='UTF-8') as f:
        local_json = f.read()
    return json.loads(local_json)


def check_config_json():
    try:
        with open('config.json', 'r', encoding='UTF-8') as f:
            local_json = f.read()
            print('[config.json] File exists')

        all_json = json.loads(local_json)
        servers_list = all_json['servers']
        healthchecks_list = all_json['healthchecks']

        for idx, server in enumerate(servers_list):
            # 判断是否存在字段
            if not (server.__contains__('username')
                    and server.__contains__('name')
                    and server.__contains__('type')
                    and server.__contains__('host')
                    and server.__contains__('location')
            ):
                print(f"[config.json] servers[{idx}] Missing key")
                return False

        # 获取本地 healthchecks_list 列表
        for idx, check in enumerate(healthchecks_list):
            # 判断是否存在字段
            if not (check.__contains__('name')
                    and check.__contains__('token')
                    and check.__contains__('period')
                    and check.__contains__('grace')
            ):
                print(f"[config.json] healthchecks[{idx}] Missing key")
                return False

    except json.decoder.JSONDecodeError as e:
        print(f"[config.json] Format test failed: {e}")
        return False
    except FileNotFoundError as e:
        print("[config.json] Doesn't exist")
    print('[config.json] Format test passed')
    return True


def get_local_json():
    # 读取本地config.json
    all_json = load_config_json()
    # 获取本地 servers_list healthchecks_list 列表
    servers_list = all_json['servers']
    healthchecks_list = all_json['healthchecks']

    # 处理 servers_list 数据
    for idx, server in enumerate(servers_list):
        # 判断是否禁用 disable
        has_disable = server.__contains__('disable')
        if has_disable and server['disable']:
            del servers_list[idx]
            continue

        # 添加默认数据，online4 online6为False
        server['online4'] = False
        server['online6'] = False
        # 删除 老版json 无用字段
        if server.__contains__('password'):
            del server['password']

    # 处理 healthchecks_list 数据
    for idx, check in enumerate(healthchecks_list):
        # 判断是否禁用 disable
        has_disable = check.__contains__('disable')
        if has_disable and check['disable']:
            del healthchecks_list[idx]
            continue

    # pprint(all_json)
    # pprint(servers_list)
    print('[config.json] Data processing is complete')
    return all_json, servers_list, healthchecks_list


if __name__ == '__main__':
    check_config_json()
    get_local_json()
    pass
