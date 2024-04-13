import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { IVehicle, VehicleService } from '../../services/vehicle.service';
import { MatIconModule } from '@angular/material/icon';
import { MatDividerModule } from '@angular/material/divider';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

interface IVehicleObject extends IVehicle {
  speed: number | null
  isMonitoring: boolean
}

@Component({
  selector: 'app-vehicles',
  standalone: true,
  imports: [MatTableModule, MatPaginatorModule, MatButtonModule, MatDividerModule, MatIconModule, MatCardModule, MatDialogModule, FormsModule, MatInputModule, MatFormFieldModule],
  templateUrl: './vehicles.component.html',
  styleUrl: './vehicles.component.scss'
})

export class VehiclesComponent {
  displayedColumns: string[] = ['name', 'speed', 'action'];
  dataSource = new MatTableDataSource<IVehicleObject>([]);
  editingVehicle: IVehicle | null = null

  constructor(private vehicleService: VehicleService, private dialog: MatDialog) { }

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild('removeComfirmDialog') removeComfirmDialog: any;
  @ViewChild('formDialog') formDialog: any;

  ngAfterViewInit() {
    this.fetchData()
    this.dataSource.paginator = this.paginator;
    this.initSocket()
  }

  fetchData() {
    this.vehicleService.getAll().subscribe(
      data => this.dataSource.data = data.map(e => Object.assign({}, e, { speed: null, isMonitoring: false }))
    )
  }

  initSocket() {
    this.vehicleService.getSpeed().subscribe((result) => {
      const target = this.dataSource.data.find(e => e.id === result.id)
      console.log(target)
      if (target) {
        Object.assign(target, { speed: result.speed, isMonitoring: true })
        this.dataSource._updateChangeSubscription()
      }
    });
  }

  create() {
    const dialogRef = this.dialog.open(this.formDialog, {
      data: { id: '', name: '' },
    })

    dialogRef.afterClosed().subscribe(result => {
      this.vehicleService.add(result).subscribe(
        _ => {
          this.fetchData()
        }
      )
    })
  }

  update(req: IVehicleObject) {
    const dialogRef = this.dialog.open(this.formDialog, {
      data: JSON.parse(JSON.stringify(req)),
    })

    dialogRef.afterClosed().subscribe(result => {
      this.vehicleService.update(result).subscribe(
        data => {
          const index = this.dataSource.data.findIndex(e => e.id === data.id)
          this.dataSource.data.splice(index, 1, Object.assign({}, req, data))
          this.dataSource._updateChangeSubscription()
        }
      )
    })
  }

  remove(req: IVehicleObject) {
    const dialogRef = this.dialog.open(this.removeComfirmDialog, {
      data: req,
    })

    dialogRef.afterClosed().subscribe(confirm => {
      if (confirm) {
        this.vehicleService.remove(req.id).subscribe(
          _ => {
            const index = this.dataSource.data.findIndex(e => e.id === req.id)
            this.dataSource.data.splice(index, 1)
            this.dataSource._updateChangeSubscription()
          }
        )
      }
    })
  }

  monitorSpeed(req: IVehicleObject) {
    this.vehicleService.monitorSpeed(req.id)
    req.isMonitoring = true
    this.dataSource._updateChangeSubscription()
  }

  stopMonitorSpeed(req: IVehicleObject) {
    this.vehicleService.stopMonitorSpeed(req.id)
    req.isMonitoring = false
    this.dataSource._updateChangeSubscription()
  }
}
