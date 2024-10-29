import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableauDashboardComponent } from './tableau-dashboard.component';

describe('TableauDashboardComponent', () => {
  let component: TableauDashboardComponent;
  let fixture: ComponentFixture<TableauDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableauDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TableauDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
