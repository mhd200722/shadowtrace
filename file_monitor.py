import ctypes
from datetime import datetime
import time
from pyfiglet import figlet_format
from termcolor import colored



#--------Utilities-------

def filetime_to_datetime(filetime_value):
    EPOCH_DIFF = 116444736000000000 
    
    if filetime_value == 0:
        return None
    
    timestamp = (filetime_value - EPOCH_DIFF) / 10000000.0
    
    try:
        return datetime.fromtimestamp(timestamp)
    except (ValueError, OSError):
        return None
    
def format_file_size(size_bytes):

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

#--------- C Structures -------
class Record (ctypes.Structure):
    
    _fields_=[("file_name",ctypes.c_char_p),("full_path",ctypes.c_char_p),("file_size",ctypes.c_longlong),("creation_time",ctypes.c_longlong),("last_access_time",ctypes.c_longlong),("modified_time",ctypes.c_longlong)]

class Collection(ctypes.Structure):
    _fields_=[("records",ctypes.POINTER(Record)),("num_of_record",ctypes.c_int),("max_num_of_record",ctypes.c_int)]    

# -----------Scan From C library-------

clibrary=ctypes.CDLL("./file_scanner.dll")

#-------- Scan Directory Path To get The Data From C -------
def scan_dir_py (directory_path):
    
    clibrary.Intilize.restype = ctypes.POINTER(Collection)
    clibrary.Intilize.argtypes = []
    Collection_ptr=clibrary.Intilize()
    if not Collection_ptr:
        print(colored("Failed to initialize collection",color="red"))
        return []
    
    path_bytes = directory_path.encode('utf-8')
    
    clibrary.Scan_Directory(Collection_ptr, path_bytes)
    clibrary.Scan_Directory.restype=None
    
    file_records=[]
    num_records=Collection_ptr.contents.num_of_record
    
    
    for i in range(num_records):
        record=Collection_ptr.contents.records[i]
        
        file_info={
            'file_name':record.file_name.decode('utf-8') if record.file_name else "",
            'full_path':record.full_path.decode('utf-8') if record.full_path else "",
            'file_size':record.file_size,
            'creation_time': filetime_to_datetime(record.creation_time),
            'last_access_time': filetime_to_datetime(record.last_access_time),
            'modified_time': filetime_to_datetime(record.modified_time),
            'creation_time_raw': record.creation_time,
            'last_access_time_raw': record.last_access_time,
            'modified_time_raw': record.modified_time
        }
        
        file_records.append(file_info)
        
        
        
    clibrary.CleanUp.restype = None
    clibrary.CleanUp.argtypes = [ctypes.POINTER(ctypes.POINTER(Collection))]
    clibrary.CleanUp(ctypes.byref(Collection_ptr))
        
    return file_records
# -------- Create A Snapshot for Every File by Key (Path_file)-----------
def create_snapshot(file_records):
    snapshot={}
    for file_info in file_records:
        snapshot[file_info['full_path']]=file_info
    return snapshot

# -------- Detect any Added Or Modified Or Deleted Files------    
def detect_anychanges(old_snapshot,new_snapshot):
    added=[]
    deleted=[]
    modified=[]
    
    old_files=set(old_snapshot.keys())
    new_files=set(new_snapshot.keys())
    
    for f in new_files-old_files:
        added.append(new_snapshot[f])
    for f in old_files-new_files:
        deleted.append(old_snapshot[f])
    for f in old_files&new_files:
        old_file=old_snapshot[f]
        new_file=new_snapshot[f]
        if old_file['file_size']!=new_file['file_size'] or old_file['modified_time']!=new_file['modified_time'] :
            modified.append(new_file);
    return added,deleted,modified             

#--------- Update Behavior Profile To Check any modification in Size or time-----
behavior_profile={}
def update_behavior_profile(snapshot):
    
    for path ,file_info in snapshot.items():
        if path not in behavior_profile:
            behavior_profile[path]={
                'mod_count':0,
                'SizeHistory_list':[],
                'last_modified': file_info['modified_time']
            }
        last_mod=behavior_profile[path]['last_modified']
        
        if file_info['modified_time']!=last_mod:
            behavior_profile[path]['mod_count']+=1
            behavior_profile[path]['last_modified']=file_info['modified_time']
        behavior_profile[path]['SizeHistory_list'].append(file_info['file_size'])    

# --------- Detect Anomalies Files --------------

        
def detect_anomalies (snapshot,behavior_profile,mod_threshold=3,growth_fator=2.0):
    anomalies=[]
    for path,file_info in snapshot.items():
        profile=behavior_profile.get(path)
        if not profile:
            continue
        
        if profile['mod_count']>mod_threshold:
            anomalies.append(f"File modified too often : {path} ({profile['mod_count'] } times )")
        
        if len(profile['SizeHistory_list'])>=2:
            prev_size=profile['SizeHistory_list'][-2]
            curr_size=profile['SizeHistory_list'][-1]
            if prev_size>0 and curr_size/prev_size>=growth_fator:
                anomalies.append(f"File grew suddenly: {path} ({format_file_size(prev_size)} -> {format_file_size(curr_size)})")
            
    return anomalies    

# -------------Monitor Directory ----------------
def monitor_directory(directory_path,number_of_scans=10,scan_interval=60):
    file_history=[]
    all_anomalies = []  
    all_added = []
    all_deleted = []
    all_modified = []
    
    print(colored(f"\n🔍 Starting scan 1/{number_of_scans}...", color="cyan"))
    for i in range(number_of_scans):
        print(colored(f"\n📊 Scan {i+1}/{number_of_scans} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", color="cyan"))
        file_records=scan_dir_py(directory_path)
        snapshot=create_snapshot(file_records=file_records)
        file_history.append(snapshot)
        update_behavior_profile(snapshot)
        if len(file_history) >= 2:
            added, deleted, modified = detect_anychanges(file_history[-2], file_history[-1])
            if added: 
                print(colored(f"✅ Added files: {len(added)}", color="blue"))
                for f in added:
                    print(colored(f"   + {f['full_path']}", color="blue"))
                all_added.extend(added)
                
            if deleted: 
                print(colored(f"🗑️  Deleted files: {len(deleted)}", color="cyan"))
                for f in deleted:
                    print(colored(f"   - {f['full_path']}", color="cyan"))
                all_deleted.extend(deleted)
                
            if modified: 
                print(colored(f"📝 Modified files: {len(modified)}", color="yellow"))
                for f in modified:
                    print(colored(f"   ~ {f['full_path']}", color="yellow"))
                all_modified.extend(modified)
                
        anomalies=detect_anomalies(snapshot,behavior_profile)
        
        if anomalies:
            print(colored(f"\n⚠️  ANOMALIES DETECTED: {len(anomalies)}", color="red"))
            for a in anomalies:
                print(colored(f"   ⚠️  {a}", color="red"))
            all_anomalies.extend(anomalies)
        else:
            print(colored("✓ No anomalies detected in this scan", color="green"))
        
        MAX_SNAPSHOT_HISTORY = 10     
        if len(file_history) > MAX_SNAPSHOT_HISTORY:
            file_history.pop(0)
        
        if i < number_of_scans - 1:  # Don't sleep after last scan
            print(colored(f"⏳ Waiting {scan_interval} seconds until next scan...", color="white"))
            time.sleep(scan_interval)
    return {
        'anomalies': all_anomalies,
        'added': all_added,
        'deleted': all_deleted,
        'modified': all_modified,
        'total_scans': number_of_scans,
        'directory': directory_path
            
    }