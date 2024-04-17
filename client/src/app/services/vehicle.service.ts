import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import io from 'socket.io-client';
import { Observable } from 'rxjs';

export interface IVehicle {
  id: string
  name: string
}

export interface ISpeedSimulation {
  id: string,
  speed: number
}

@Injectable({
  providedIn: 'root'
})
export class VehicleService {

  private apiBaseUrl = import.meta.env['NG_APP_API_BASE_URL']
  private socket = io(`${this.apiBaseUrl}`);

  constructor(private http: HttpClient) { }
  

  getAll() {
    return this.http.get<IVehicle[]>(`${this.apiBaseUrl}/api/vehicles`)
  }

  add(body: IVehicle) {
    return this.http.post<IVehicle>(`${this.apiBaseUrl}/api/vehicles`, body)
  }

  update(body: IVehicle) {
    return this.http.put<IVehicle>(`${this.apiBaseUrl}/api/vehicles/${body.id}`, body)
  }

  remove(id: string) {
    return this.http.delete(`${this.apiBaseUrl}/api/vehicles/${id}`)
  }

  monitorSpeed(id: string) {
    this.socket.emit('monitor_start', id)
  }

  stopMonitorSpeed(id: string) {
    this.socket.emit('monitor_end', id) 
  }

  getSpeed() {
    let observable = new Observable<{ id: string, speed: number }>((observer: any) => {
      this.socket.on('speed', (data: ISpeedSimulation) => {
        observer.next(data);
      });
      return () => { this.socket.disconnect(); };  
    });
    return observable;
  }
}
