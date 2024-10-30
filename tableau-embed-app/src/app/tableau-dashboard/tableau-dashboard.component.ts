import { Component, OnInit } from '@angular/core';
import { TableauService } from './tableau.service';


@Component({
  selector: 'app-tableau-dashboard',
  template: `
    <div id="tableau-container"></div>
  `,
  styles: []
})
export class TableauDashboardComponent implements OnInit {
  constructor(private tableauService: TableauService) {}

  ngOnInit() {
    this.tableauService.getEmbedUrl('WorldIndicators', 'Tourism')
      .subscribe(embedUrl => {
        this.initTableauEmbed(embedUrl);
      });
  }

  initTableauEmbed(embedUrl: string) {
    const containerDiv = document.getElementById('tableau-container');
    const options = {
      hideTabs: true,
      hideToolbar: true,
      width: '100%',
      height: '600px'
    };
    const viz = new window.tableau.Viz(containerDiv, embedUrl, options);
  }
}
