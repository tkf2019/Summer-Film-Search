from filecmp import cmp
from functools import cmp_to_key
import json
import os
import time
import functools
from django.http import JsonResponse

def search(request):
    if request.method == 'GET':
        start = time.time()
        keyword = request.GET['keys']
        keytype = request.GET['type']
        pack_size = int(request.GET['packSize'])
        pack_index = int(request.GET['packIndex'])
        
        json_results = []
        set_aux = set()
        if keytype == 'Movies':
            json_files = os.listdir(os.path.abspath('filmdata'))
            for json_file in json_files:
                fp = open(os.path.abspath('filmdata') + '/' + json_file, 'r', encoding='utf8')
                try:
                    json_result = json.load(fp)
                except ValueError:
                    continue
                fp.close()
                name = json_result['name']
                i = json_result['id']
                if keyword in name and i not in set_aux:
                    set_aux.add(i)
                    json_results.append({
                        'name': json_result['name']  + '（' + json_result['score'] + '分）',
                        'score': json_result['score'],
                        'id': i,
                        'image': json_result['image']
                    })
                else:
                    for actor in json_result['actor']:
                        try:
                            afp = open(os.path.abspath('stardata') + '/' + actor + '.json', 'r', encoding='utf8')
                        except FileNotFoundError:
                            continue
                        try:
                            actor_json = json.load(afp)
                        except ValueError:
                            continue
                        afp.close()
                        if keyword in actor_json['name'] and i not in set_aux:
                            set_aux.add(i)
                            json_results.append({
                                'name': json_result['name']  + '（' + json_result['score'] + '分）',
                                'score': json_result['score'],
                                'id': json_result['id'],
                                'image': json_result['image']
                            })
            json_results.sort(key=lambda file: file['score'], reverse=True)
        elif keytype == 'Stars':
            json_files = os.listdir(os.path.abspath('stardata'))
            for json_file in json_files:
                fp = open(os.path.abspath('stardata') + '/' + json_file, 'r', encoding='utf-8')
                try:
                    json_result = json.load(fp)
                except ValueError:
                    continue
                fp.close()
                name = json_result['name']
                i = json_result['id']
                if keyword in name and i not in set_aux:
                    set_aux.add(i)
                    json_results.append({
                        'name': json_result['name'],
                        'id': json_result['id'],
                        'image': json_result['image']
                    })
                else:
                    for movie in json_result['movies']:
                        try:
                            mfp = open(os.path.abspath('filmdata') + '/' + movie + '.json', 'r', encoding='utf-8')
                        except  FileNotFoundError:
                            continue
                        try:
                            movie_json = json.load(mfp)
                        except ValueError:
                            continue
                        mfp.close()
                        if keyword in movie_json['name'] and i not in set_aux:
                            set_aux.add(i)
                            json_results.append({
                                'name': json_result['name'],
                                'id': json_result['id'],
                                'image': json_result['image']
                            })
        elif keytype == 'Comments':
            json_files = os.listdir(os.path.abspath('filmdata'))
            for json_file in json_files:
                fp = open(os.path.abspath('filmdata') + '/' + json_file, 'r', encoding='utf-8')
                try:
                    json_result = json.load(fp)
                except  ValueError:
                    continue
                fp.close()
                for comment in json_result['comment']:
                    if keyword in comment:
                        times = comment.count(keyword)
                        json_results.append({
                                'id': json_result['id'],
                                'name': json_result['name'],
                                'score': json_result['score'],
                                'image': json_result['image'],
                                'times': times,
                                'comment': comment
                            })
            def mycmp(n1, n2):
                
                if n1['times'] == n2['times']:
                    if n1['score'] < n2['score']:
                        return 1
                    elif n1['score'] == n2['score']:
                        return 0
                    else:
                        return -1
                elif n1['times'] < n2['times']:
                    return 1
                else:
                    return -1
            json_results.sort(key=functools.cmp_to_key(mycmp))
        
        total_time = format(time.time() - start, '.8f')
        return JsonResponse({
            'time': str(total_time) + 's',
            'number': len(json_results),
            'results': json_results[(pack_index - 1) * pack_size:pack_index * pack_size] 
        })

def info(request):
    err = JsonResponse({
        'error': 'Something Wrong Happened'
    })
    if request.method == 'GET':
        info_type = request.GET['type']
        info_id = request.GET['id']
        if info_type == 'Movies' or info_type == 'Comments':
            try:
                fp = open(os.path.abspath('filmdata') + '/' + info_id + '.json', 'r', encoding='utf-8')               
                json_result = json.load(fp)
            except ValueError or FileNotFoundError:
                return err
            fp.close()
            actor_list = []
            for actor in json_result['actor']:
                try:
                    afp = open(os.path.abspath('stardata') + '/' + actor + '.json', 'r', encoding='utf-8')
                    actor_json = json.load(afp)
                except ValueError or FileNotFoundError:
                    continue
                afp.close()
                actor_list.append({
                    'name': actor_json['name'],
                    'id': actor,
                    'image': actor_json['image']
                })
            try:
                language = json_result['language']
            except KeyError:
                language = ''
            try:
                date = json_result['date']
            except KeyError:
                date = ''
            try:
                time = json_result['time']
            except KeyError:
                time = ''
            return JsonResponse({
                'id': info_id,
                'name': json_result['name'],
                'image': json_result['image'],
                'score': json_result['score'],
                'director': json_result['director'],
                'author': json_result['author'],
                'actor': actor_list,
                'genre': json_result['genre'],
                'location': json_result['location'][0],
                'language': language,
                'date': date,
                'time': time,
                'description': json_result['description'],
                'comment': json_result['comment']
            })
        elif info_type == 'Stars':
            try:
                fp = open(os.path.abspath('stardata') + '/' + info_id + '.json', 'r', encoding='utf-8')
                json_result = json.load(fp)
            except ValueError or FileNotFoundError:
                return err
            fp.close()
            related_list = []
            for actor in json_result['cooperators']:
                number = json_result['cooperators'][actor]
                try:
                    afp = open(os.path.abspath('stardata') + '/' + actor + '.json', 'r', encoding='utf-8')
                    actor_json = json.load(afp)
                except ValueError or FileNotFoundError:
                    continue
                afp.close()
                related_list.append({
                    'id': actor,
                    'name': actor_json['name'],
                    'number': number,
                    'image': actor_json['image']
                })
            movie_list = []
            for movie in json_result['movies']:
                try:
                    afp = open(os.path.abspath('filmdata') + '/' + movie + '.json', 'r', encoding='utf-8')
                    movie_json = json.load(afp)
                except ValueError or FileNotFoundError:
                    continue
                afp.close()
                movie_list.append({
                    'name': movie_json['name']  + '（' + movie_json['score'] + '分）',
                    'score': movie_json['score'],
                    'id': movie,
                    'image': movie_json['image']
                })
            movie_list.sort(key=lambda movie: movie['score'], reverse=True)
            try:
                birth_death = json_result['birth-death']
            except KeyError:
                birth_death = ''
            try:
                place = json_result['place']
            except KeyError:
                place = ''
            try:
                occupation = json_result['occupation']
            except KeyError:
                occupation = ''
            print(json_result['image'])
            return JsonResponse({
                'id': info_id,
                'name': json_result['name'],
                'image': json_result['image'],
                'gender': json_result['gender'],
                'birthDeath': birth_death,
                'place': place,
                'occupation': occupation,
                'movie': movie_list,
                'description': json_result['description'],
                'cooperator': related_list[:10]
            })