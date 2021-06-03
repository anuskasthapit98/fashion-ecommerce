(function(){
        
    var isAdvancedUpload = function() {
        var div = document.createElement('div');
        return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
    }();

    if (isAdvancedUpload) {
        $('.upload-box').addClass('has-advanced-upload');

        var droppedFiles = false;

        $('.upload-box').on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
            e.preventDefault();
            e.stopPropagation();
        })
        .on('dragover dragenter', function() {
            $(this).addClass('is-dragover');
        })
        .on('dragleave dragend drop', function() {
            $(this).removeClass('is-dragover');
        })
        .on('drop', function(e){
            droppedFiles = e.originalEvent.dataTransfer.files;
            $(this).find('input[type="file"]').prop('files', droppedFiles);
            loadFiles(this, droppedFiles );
        });

        $('body').on('click', '.upload-box .upload-box-input', function(e){
            e.preventDefault();
            e.stopPropagation();
            $(this).parents('.upload-box').find('input[type="file"]').click();
        })
        
        $('body').on('click', '.upload-file-content', function(e){
            e.preventDefault();
            e.stopPropagation();
        });

        $('.upload-box input[type="file"]').on('change', function(e) {
            e.preventDefault();
            e.stopPropagation();
            var parent = $(this).parents('.upload-box').get();
            loadFiles(parent, e.target.files);
        });

        $('.upload-box').submit(function(event){
            event.preventDefault();

            var form_data = new FormData();
            form_data.append('file', $('#id_file')[0].files[0]);
            
            $button.attr('disabled', 'true');

            $.ajax({
                url: '#',
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
                },
                data: form_data,
                processData: false,
                contentType: false,
                xhr: function() {
                    var xhr = new window.XMLHttpRequest();
                    xhr.upload.addEventListener("progress", function(evt) {
                        if (evt.lengthComputable) {
                            $button.text('Uploading '+ Math.round( 100 * evt.loaded / evt.total) + '%');
                            //  console.log('upload', evt.loaded / evt.total);
                        }
                    }, false);

                    xhr.addEventListener("progress", function(evt) {
                        if (evt.lengthComputable) {
                            // console.log(evt.loaded / evt.total);
                        }
                    }, false);

                    return xhr;
                },
            })
            .done(function(data, statusText, xhr) {
                console.log('File uploaded successfully.');
                $button.text('Uploaded');
            })
            .fail(function(xhr) {
                $button.text('Upload failed');  
                
                console.log('Error File upload failed.', xhr.status);
                if(xhr.responseJSON != undefined){
                    console.log(xhr.responseJSON.message);
                    alert(xhr.responseJSON.message);
                }

            })
            .always(function(){
            });

        });


        $('body').on('click', '.upload-file-remove', function(e){
            e.preventDefault();
            e.stopPropagation();
            if(typeof $(this).parents('.upload-file-content').data('pk') == typeof undefined){
                $(this).parents('.upload-file-content').remove();
            }
            else{
                removeFile($(this).parents('.upload-file-content').data('pk'));
            }
        })

    }


    getHumanizeSize = function(bytes) {
        const threshold = 1024;

        if (Math.abs(bytes) < threshold) {
            return [bytes, 'B'];
        }

        const units = ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        let u = -1;
        const r = 10;

        do {
            bytes /= threshold;
            ++u;
        } while (Math.round(Math.abs(bytes) * r) / r >= threshold && u < units.length - 1);

        return [bytes.toFixed(1), units[u]];
    }

    loadImageFromFile = function($element, file){
        console.log($element, file)
        if (file.type.startsWith('image/')) {
            var reader = new FileReader();
            
            reader.onload = function(e) {
                $element.attr('src', e.target.result);
            }
            
            reader.readAsDataURL(file); // convert to base64 string
        }
    }

    loadFiles = function(uploadBox, files) {
        $uploadFilesList = $(uploadBox).find('.upload-files-list');
        console.log($uploadFilesList);
        for(var i=0; i < files.length; i++){
            var file = files[i];
            var timeid = Date.now();
        
            $fileElement = $(`
                <div class="upload-file-content" data-timeid="${ timeid }">
                    <div class="upload-file-preview upload-image-preview">
                        <div class="upload-image">
                            <img src="#">
                        </div>
                        <div class="upload-file-details">
                            <div class="upload-file-size"></div>
                            <div class="upload-file-name"><span></span></div>
                        </div>
                        <div class="upload-progress-bar">
                            <div class="progress progress-sm">
                                <div class="progress-bar progress-bar-striped active" role="progressbar"
                                aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width:0%"></div>
                            </div> 
                        </div>
                        <div class="upload-error" style="display: none;">
                            <svg aria-hidden="true" focusable="false" data-prefix="fas" data-icon="exclamation-triangle" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" class="svg-inline--fa fa-exclamation-triangle fa-w-18 fa-2x">
                                <path fill="currentColor" d="M569.517 440.013C587.975 472.007 564.806 512 527.94 512H48.054c-36.937 0-59.999-40.055-41.577-71.987L246.423 23.985c18.467-32.009 64.72-31.951 83.154 0l239.94 416.028zM288 354c-25.405 0-46 20.595-46 46s20.595 46 46 46 46-20.595 46-46-20.595-46-46-46zm-43.673-165.346l7.418 136c.347 6.364 5.609 11.346 11.982 11.346h48.546c6.373 0 11.635-4.982 11.982-11.346l7.418-136c.375-6.874-5.098-12.654-11.982-12.654h-63.383c-6.884 0-12.356 5.78-11.981 12.654z" class=""></path>
                            </svg>
                        </div>
                    </div>
                    <a href="#" class="upload-file-remove">Remove file</a>
                </div>
            `);

            $fileElement.find('.upload-file-name span').text(file.name)
            $fileElement.find('.upload-file-size').html(`<strong>${ getHumanizeSize(file.size)[0] }</strong> ${ getHumanizeSize(file.size)[1] }`)
            if(!file.type.startsWith('image/')){
                $fileElement.find('.upload-image').remove();
            }else{
                loadImageFromFile($fileElement.find('.upload-image img'), file);
            }

            $uploadFilesList.append($fileElement);

            uploadFile(file, timeid)
        }
    };

    uploadFile = function(file, timeid){
        var formData = new FormData();
        formData.append('image', file);
        $.ajax({
            url: '{% url "dashboard:product-image-create" %}',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content'),
            },
            data: formData,
            processData: false,
            contentType: false,
            xhr: function() {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var uploadPercentage = Math.round( 100 * evt.loaded / evt.total);
                        $(`.upload-file-content[data-timeid="${timeid}"] .progress-bar`).css('width', uploadPercentage+'%').attr('aria-valuenow', uploadPercentage);
                        //  console.log('upload', evt.loaded / evt.total);
                    }
                }, false);

                xhr.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        // console.log(evt.loaded / evt.total);
                    }
                }, false);

                return xhr;
            },
        })
        .done(function(data, statusText, xhr) {
            console.log('File uploaded successfully.');
            console.log(data);

            // updating data-pk
            $(`.upload-file-content[data-timeid="${timeid}"]`).attr('data-pk', data.pk).data('pk', data.pk);

            // updating file url on name
            $(`.upload-file-content[data-timeid="${timeid}"]`).find('.upload-file-name').attr('data-url', data.url).data('url', data.url);

            // updating selection
            var $select = $(`.upload-file-content[data-timeid="${timeid}"]`).parents('.upload-box').find('.upload-file-select');
            console.log($select);
            $select.append(`<option value="${data.pk}">${data.pk}</option>`);
            var values = $select.val();
            values.push(data.pk);
            $select.val(values);
        })
        .fail(function(xhr) {
            console.log('Error File upload failed.', xhr.status);
            if(xhr.responseJSON != undefined){
                console.log(xhr.responseJSON.message);
                alert(xhr.responseJSON.message);
            }
            $(`.upload-file-content[data-timeid="${timeid}"] .upload-error`).show();
        })
        .always(function(){
            $(`.upload-file-content[data-timeid="${timeid}"] .upload-progress-bar`).remove();
        });
    }

    removeFile = function(pk){
        console.log('Deleting', pk);
        var $select = $(`.upload-file-content[data-pk="${pk}"]`).parents('.upload-box').find('.upload-file-select');
        $(`.upload-file-content[data-pk="${pk}"]`).remove();
        loadDocumentSelect($select);

        /* 
        // alternative delete technique
        var values = $select.val();
        values.splice(values.indexOf(pk), 1);
        $select.val(values);
        */
    }

    loadDocumentSelect = function($select){
        $select.empty();
        var values = [];
        $contents = $select.parents('.upload-box').find('.upload-file-content');
        for(var i=0; i < $contents.length; i++){
            $content = $($contents[i]);
            values.push($content.data('pk'));
            $select.append(`<option value="${$content.data('pk')}">${$content.data('pk')}</option>`);
        }
        $select.val(values);
    }

    $(document).ready(function(){
        $('.upload-box .upload-file-select').each(function(index, element){
            loadDocumentSelect($(element));
        });
    });
})();