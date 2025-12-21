import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RentOrSellPage } from './rent-or-sell-page';

describe('RentOrSellPage', () => {
  let component: RentOrSellPage;
  let fixture: ComponentFixture<RentOrSellPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RentOrSellPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RentOrSellPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
