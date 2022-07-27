import latis

query = latis.query(dataset='kyoto_dst_index', selection='time>=2022-07-20')
print(query)
data = latis.formatDataPd(dataset='kyoto_dst_index',
                          selection='time>=2022-07-20')
print(data)
