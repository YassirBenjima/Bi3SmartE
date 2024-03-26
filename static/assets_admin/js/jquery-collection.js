(function ($, window) {
    $.fn.collection = function (options) {
        var label = options.label ?? 'item';
        $(this).each(function (_, collection) {
            var prototype = $(collection).data('prototype');
            var prototype_name = $(collection).data('prototype-name');
            var prototype_label_name = $(collection).data('prototype-label-name');
            var allow_add = $(collection).data('allow-add');
            var allow_delete = $(collection).data('allow-delete');
            var collectionActions = $('<div class="collection-actions form-group mt-5"></div>');

            $(collection).find(' > div[id]').each(function (_, item) {
                if (allow_delete) {
                    var delete_button = $(`
                            <button type="button" class="btn btn-sm btn-icon btn-light-danger">
                                <span class="svg-icon svg-icon-1">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <rect opacity="0.5" x="7.05025" y="15.5356" width="12" height="2" rx="1" transform="rotate(-45 7.05025 15.5356)" fill="currentColor"></rect>
                                        <rect x="8.46447" y="7.05029" width="12" height="2" rx="1" transform="rotate(45 8.46447 7.05029)" fill="currentColor"></rect>
                                    </svg>
                                </span>
                            </button>
                        `);

                    delete_button.on('click', function (event) {
                        item.remove();

                        item.trigger('collection-delete', [{allow_delete, allow_add, index, originEvent: event}]);
                    });

                    delete_button.appendTo(item);
                }
            })

            // var collectionItemContainer;
            // if ($(collection).find('.collection-item-container').length === 0) {
            //     collectionItemContainer = $('<div class="collection-item-container"></div>');
            //     $(collection).append(collectionItemContainer);
            // } else {
            //     collectionItemContainer = $($(collection).find('.collection-item-container')[0]);
            // }

            if (allow_add) {
                var add_button = $(`
                    <button type="button" class="btn btn-sm btn-light-primary collection-action-add">
                        <span class="svg-icon svg-icon-2">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect opacity="0.5" x="11" y="18" width="12" height="2" rx="1" transform="rotate(-90 11 18)" fill="currentColor"></rect>
                                <rect x="6" y="11" width="12" height="2" rx="1" fill="currentColor"></rect>
                            </svg>
                        </span>
                        Add another ${prototype_label_name}
                    </button>
                `);
                add_button.on('click', function (event) {
                    event.preventDefault();
                    event.stopPropagation();

                    var index = $(collection).data('index') ?? (-1);
                    index++;
                    $(collection).data('index', index);

                    var item = $(prototype.replaceAll(`${prototype_name}_label`, prototype_label_name).replaceAll(prototype_name, index));

                    if (allow_delete) {
                        var delete_button = $(`
                            <button type="button" class="btn btn-sm btn-icon btn-light-danger">
                                <span class="svg-icon svg-icon-1">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <rect opacity="0.5" x="7.05025" y="15.5356" width="12" height="2" rx="1" transform="rotate(-45 7.05025 15.5356)" fill="currentColor"></rect>
                                        <rect x="8.46447" y="7.05029" width="12" height="2" rx="1" transform="rotate(45 8.46447 7.05029)" fill="currentColor"></rect>
                                    </svg>
                                </span>
                            </button>
                        `);

                        delete_button.on('click', function (event) {
                            item.remove();

                            $(collection).trigger('collection-delete', [{allow_delete, allow_add, index, originEvent: event, item}]);
                        });

                        item.append(delete_button);
                    }
                    $(collection).append(item);
                    $(collection).trigger('collection-add', {allow_delete, allow_add, index, originEvent: event, item});
                });
                collectionActions.append(add_button);
            }

            $(collection).after(collectionActions);
            $(collection).trigger('collection-init', [{allow_delete, allow_add}]);
        });
    }
})(jQuery, window);
