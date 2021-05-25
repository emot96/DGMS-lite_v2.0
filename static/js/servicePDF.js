function genPDF(){
    var doc = new jsPDF('p', 'pt', 'a4', true);
    var imgData='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD//gAfQ29tcHJlc3NlZCBieSBqcGVnLXJlY29tcHJlc3P/2wCEAAQEBAQEBAQEBAQGBgUGBggHBwcHCAwJCQkJCQwTDA4MDA4MExEUEA8QFBEeFxUVFx4iHRsdIiolJSo0MjRERFwBBAQEBAQEBAQEBAYGBQYGCAcHBwcIDAkJCQkJDBMMDgwMDgwTERQQDxAUER4XFRUXHiIdGx0iKiUlKjQyNEREXP/CABEIAHAAXAMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAHCAAGAgQFAwH/2gAIAQEAAAAAZi3SZaO39kyXph7pJpBO+3ySKkebpMV+0KqyNrkVI83SCQHX2nb7T7UVI83TkKXzdry1DqboqR5ugVAs3NOdhw9lUjzdFVovphn5xtLgqR5uikVIzCAzhGNIQFSPN0XsPsCNSoCdBy+mqR5umoobc7sXC3GKKkebpOL4WGDwhfYqR5ulL0gblfbMsrodhUjzc1BxDFz7Zuo7SRUiPb675dby4Vs1elF6/8QAGwEAAgIDAQAAAAAAAAAAAAAABAUCBgADBwH/2gAIAQIQAAAAWkoGJyVzo5W26WnZ0pTK0msufbfT3TOrOQiJM5PQC6iVlxBBrP8A/8QAGgEBAAIDAQAAAAAAAAAAAAAABQQGAAIDAf/aAAgBAxAAAAA2RmYMz3KiWMJMCvcr1HTomuLpp1dmDJ9TWM86iy7rTNtiP//EACYQAAEEAgMAAQQDAQAAAAAAAAUDBAYHAQIAEDYxCBITIREUIBX/2gAIAQEAAQgAg8HjJmMjiJHNZQzHM1lDMczWUMxzasIZr8uYDAWeUcOsVnC8/GayhmOZrKGY5msoZjm1YQzX5mo1mIkxMcPq7xgr/BIi2FNN3TgmTclXW7lzEZP9/wBgsh/ix/ZmuVd4wV24cJNEVF1phK9nK2VeN8bpNk/zsD26bxT88SkOhNDVo67sf2ZrlXeMFdz6T6J4UZ6NMqlCyO6626Ouv2ryLZLRVBojFjy7JyglwQVSJj0HaXVj+zNcq7xgrqRlsCxqyyZshl872xq3crtdtt0GGVHJJplUg4/tPXC3MZzjOM4riSZwtq3V6sf2ZrlXeMFdWmZyjumyT6ZKfhUVWx0DfbMX6W+BjzD0ezdY5Y/szXKu8YK6sV3s6k77TPE0VVs7YR/nP75okrvoopp1Xz3LyKstt+WP7M1yrvGCup0lslLDWu3Ke11y6O5y6xjDlxjEA00zBJdnPVYI7aRJnttyx/ZmuVd4wV1bgRVsTbG9MYzn9YrCPGQqxdQm4gUu3cL76wyPGR0Pkw96VCFAiqSJRu3WduEWrcEM1ECB43HLH9ma5V3jBXRsQyNDXA55IY++jZFRg9FO9Xg1i8T6txzhWRNW+K1hG7DXQ+V6sf2ZrlXeMFdn4+LkTH+mQjAx8FG6CHnNs/brtng+FaOTjuTSH47sf2ZrlXeMFdS6fR+H5bIk4hZcelr16JaVtbD2WfUDOxHKrtN/Yd5TrRsb+oeAiH5Rm3LsWNuxMGTitfxOVTac2VH+REAtFo8xCOuWP7M1yrvGCunKez+6Zh/15C6CRCOzC12Ekg8nr9nTg+MpA819YNkxuMQmdV9CvpqVSQo4E6glOgkD/wBKTVVxDpRK3XVj+zNcg84jIaMjhxHFnQzHwWkVUHlU1zShuoVh6IldzN64ePBxF1iY1lqWVPaN3FHNHyZRovYsFcoLNXIucVyDZaDg2tnwzXH61s+Ga/E1JMy8mJkR/wD/xAA8EAACAQIDBQQHBgQHAAAAAAABAgMABAUREhAhMVGzE0Fk0gZCUmFxgZQUICIjJHIHMmKxY5GSk6HC4v/aAAgBAQAJPwDDjLcymbW/bSrnplZRuVgKwk/UT+esIP1E/nrCD9RP56wo/UT+erARmV9Carmbef8AXWEn6ifz1hJ+on89YQfqJ/PWEH6ifz1hR+on89Q9lbQmHQmpmy1RKx3sSeJrxHXf7jZADJVHFmPcKb3Ig4IvIU/49whlPrZeqT93nB0ErxHXfa4WNFLMx7gK9620PIe0afNwmpyefE057CSQlT3xknd8qk/UxjPPulXn9znB0ErxHXfa/wCRCfxgevL3L8BR1EvrbkFXflTqFf8ADkxyzz7qRUVF1EKABm1SlZEbOB/+p9xo5E7nT2WHEHbzg6CV4jrvsOUjflxfvPf8qcmKMkL7z3tT6GZdJI45U7OxlUksczu30cwznT8BuFEgjeDT7psonHKX1W+e3nB0ErxHXfY+9UyHuZ+J+Q28UifT8WGkf32sVVyFJ5HuPyNHfJEpPuJ47OcHQSvEdd9h3RNo+Y3bIncgFiFUkgDiTlsidkQAuwUkLnzPdtYlhmvzzzOznB0ErxHXfZ3z6h8GAOwAkQw/8lqG4Sv/AHpAcxcA/wCyNvryysPhqI2c4OgleI677EzhuYxFIR3SJw/zGyxeBJ4oRGWKnUQTyJrBZCGkYg64+BP7qsWiubgTdlGWUltcQUcDVm1u8ilkDEHMD9pNRl5pXVEUcSzHICiCIIEQkeswG8/M7OcHQSvEdd9kYaGVcv6ge5hyIpf6opR/LIncwrhPbxyA+5lz2nfBZoCOTMxNQ6bp1/TRMN8SH1z/AFHbzg6CV4jrvthz9iQbnjb2lNSrOLVisE43a4jwBHcV4bATkOAoJNdyy6oLcb44FXcmr2mAH3OcHQSvEdd9k0st7dbraytYzNcy/tRaW7s8UtU1y2V9CYJwnPKsUmfAIrCWDD4O0JgD2MqI0qDnJmxrE5n9G7TCHiw61Eh7AiCeNPtGn2pCSQagxnF4sMOnEbzCrI3FpaH/ABZa9OsXwrD55PtUd5g832eaUAFDG5O8BTxXmK/i/wCmseEejN3HZw3CYm/azSlnRtXwMdY3iGLvbmUm9xKXtrqXtJC/5j9+nPSPds5wdBK8R132emEno5exRRR2ExSMh7fQCVQzbhzr0+mx/FYLKXArSUoiAXk+QTSUAD6AddWip6Q+k2B4hhdy5QhxPiLAvqYcGiSbTq7gKTTdYV/CWaO3khXRLLcosTNPu4ysxLVidhJi15Y38MtiHQ3M2IXOpAskfH/xSPbzx2tziFzHJuMKTO04VgeBCcaH6nHfSK6uT70Uecnbzg6CViJiuYjNrTsZWy1Ssw3qpFYsfp5/JUFhfSoCqPdYc8zKOQLxmrLDJcPhmE8VrJhZaBJQCA6oY8g1S2815YGQ2lxJZSPLAZV0OYnKZpqG45V9kXFZIuxe9Fg4uWi9gy6NRXdwrAcChv0k7VbmPBQkyye0HEWeqsQSWGVGjkjktZmRkbcVIKZEGpbaxtELFILWxkhiXUczpREAGZrFj9PP5KxU/Tz+Spu1tpjDofSy56YlU7mAPEV//8QAMREAAQMDAQUGBQUBAAAAAAAAAQIDBAAFERITNFFzsQYUISIxQSNUYWJxFVNykZLB/9oACAECAQE/AIkSKqLGUqO2SW0kkpHCu5RPlWv8Cr1Pt1qSlCYjLj6vRGkeA4mreq2XGOiQxHa+5OkZSeBruUT5Vr/Aq+RmGoqFNMoQdoBlKQPY1C3OLykdKuc9FuiqeIys+VtPFRqetxx3W8oreWdaz/wVbZrlvdbltJOyVgOt8U8fyKadQ82h1tWULAII4Gr/ALm3zR0NQtzi8pHSrzIMq4rGfhseRI+73NLSClRAGojGaSkJSE+wGK7NSFaH4SjkI87f8Veoq/7m3zR0NQ9zjcpHSn8h9/PrtF5/s07GDcWNI152pUMcNNPxtizFd152yCrHDBxVhz+oAj9tQNX/AHNvmjoahbnF5SOlXqApp8yUD4Th8cexo2iO9GjslxelGSCMZOqrvBaZgskKVlrCEfXUaskBUdtUh0YW4PAcE1f9zb5o6GoW5xeUjpTi47hMdxSCVeBSaV2fmxW30qThEeI1IVnPglzGE/mnrS6THcnsraZ1jC1oJSCRkZAq4W9u3qS33xDrhShRQlChhK06gSTV/wBzb5o6GokuKmLGSqQ2CG0ggqHCoLlvjzGn5L7TzSX9qU7TBPjnHril9s2HmtDy2lEtrCyHB51FwLTn6JAwKm9oLdIQ+204AH5feHSt1JP0SMewzVwu8OdNkS9u2kOKyElYOABgCr5JYdioS08hZ2gOEqB9jX//xAAvEQABAwICCQQABwAAAAAAAAABAgMEABEFEgYTFCE0QXOSsSJRVGIQI0JTcYGR/9oACAEDAQE/AIcOKqLGUqM0SWkEkoHtWxQ/itdgow4fxWuwVsUP4rXYK2KH8VrsFY5HjtREKbYQg60C6UgcjULg4vRR4pxxLSFOLNkpFyahS1TFSZJOVoHI2D5NQp5jy3IMl7OM3pX9jy/DSDg2+qPBqFwcXoo8Vj803TDQfsumHFBxpKlnVpVmtfdu3044pbi3CfUVFVYRM2uKMx/MR6VVpBwbfVHg1C4OL0keKxFRXOlFX7hFOxtVFjSc99aVi3tlp+NqWYrue+uSVW9rG1aOKIkPo5Fu/wDhrSDg2+qPBqFwcXoo8VjcBTUgykC7Th9X1VRweM9FjMlxeVu5SRbfmrF4DLMFkpWq7NkIvzzGsDgqjNKfdFluAWHsmtIODb6o8GoXBxeijxRwic9CXLVAdVEykqWU+nLe1/4vzptSEIQ2i9gco/qnG2XyjOAvIcwTyvSFFX6bCtIODb6o8GocyKmLGSqS0CGkAgrHtWIaaRZUBEaLITHXsbURSQWcmRAsrflz2Va9r0H4YO6W13ikyogteWzuTYWWKRLhpSE7U13isckR3YiEtvoWdaDZKgeRr//Z';
    var res = doc.autoTableHtmlToJson(document.getElementById("service-history"));


    doc.addImage(imgData, 'jpeg', 270, 10, 62, 72); 
    doc.fromHTML($("#pdfName").get(0), 240, 85, {'width': 250});
    doc.fromHTML($("#customerName").get(0), 20, 130, {'width': 180});
    doc.fromHTML($("#assetDetail").get(0), 20, 180, {'width': 180});
    doc.fromHTML($("#assetAddress").get(0), 380, 180, {'width': 250});

    var options = {
        // beforePageContent: header,
        margin: {
        left:20,
        right:20,
        top: 10
        },
        theme:'grid',
        styles: {
                overflow: 'linebreak',
                fontSize: 10,
                valign: 'middle',
                // fillColor: [255, 193, 51]
            },
            
            didParseCell: function (data) {
            
                if (data.row.index ===  3 || data.row.index ===  7) {
                    data.cell.styles.fillColor = [231, 232, 235];
                    data.cell.styles.fontStyle = "bold";
                    data.cell.styles.textColor = [139,0,139];
                    data.cell.styles.halign = "left";
                }
            },
      
        startY: doc.autoTableEndPosY() + 270
        }; 

    doc.autoTable(res.columns, res.data, options);


    const pageCount = doc.internal.getNumberOfPages();

    // For each page, print the page number and the total pages
    for(var i = 1; i <= pageCount; i++) {
     // Go to page i
    doc.setPage(i);
     //Print Page 1 of 4 for example
    doc.setFontSize(10)
    doc.text('visit us: https://www.emot.co.in/',20,830);
    doc.text('Page ' + String(i) + ' of ' + String(pageCount),577,830,null,null,"right");
    }


// Save the PDF
doc.save('service history.pdf');
doc.output('datauri');

}