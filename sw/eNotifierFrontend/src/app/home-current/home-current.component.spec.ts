import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeCurrentComponent } from './home-current.component';

describe('HomeCurrentComponent', () => {
  let component: HomeCurrentComponent;
  let fixture: ComponentFixture<HomeCurrentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomeCurrentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeCurrentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
