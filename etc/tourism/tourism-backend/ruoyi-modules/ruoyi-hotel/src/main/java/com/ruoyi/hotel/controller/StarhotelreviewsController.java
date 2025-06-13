package com.ruoyi.hotel.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.hotel.domain.Starhotelreviews;
import com.ruoyi.hotel.service.IStarhotelreviewsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 星级酒店评价Controller
 * 
 * @author ningf
 * @date 2024-07-15
 */
@RestController
@RequestMapping("/starhotelreviews")
public class StarhotelreviewsController extends BaseController
{
    @Autowired
    private IStarhotelreviewsService starhotelreviewsService;

    /**
     * 查询星级酒店评价列表
     */
    @GetMapping("/list")
    public TableDataInfo list(Starhotelreviews starhotelreviews)
    {
        startPage();
        List<Starhotelreviews> list = starhotelreviewsService.selectStarhotelreviewsList(starhotelreviews);
        return getDataTable(list);
    }

    /**
     * 导出星级酒店评价列表
     */
    @Log(title = "星级酒店评价", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Starhotelreviews starhotelreviews)
    {
        List<Starhotelreviews> list = starhotelreviewsService.selectStarhotelreviewsList(starhotelreviews);
        ExcelUtil<Starhotelreviews> util = new ExcelUtil<Starhotelreviews>(Starhotelreviews.class);
        util.exportExcel(response, list, "星级酒店评价数据");
    }

    /**
     * 获取星级酒店评价详细信息
     */
//    @RequiresPermissions("hotel:starhotelreviews:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starhotelreviewsService.selectStarhotelreviewsById(id));
    }

    /**
     * 新增星级酒店评价
     */
//    @RequiresPermissions("hotel:starhotelreviews:add")
    @Log(title = "星级酒店评价", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Starhotelreviews starhotelreviews)
    {
        return toAjax(starhotelreviewsService.insertStarhotelreviews(starhotelreviews));
    }

    /**
     * 修改星级酒店评价
     */
//    @RequiresPermissions("hotel:starhotelreviews:edit")
    @Log(title = "星级酒店评价", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Starhotelreviews starhotelreviews)
    {
        return toAjax(starhotelreviewsService.updateStarhotelreviews(starhotelreviews));
    }

    /**
     * 删除星级酒店评价
     */
//    @RequiresPermissions("hotel:starhotelreviews:remove")
    @Log(title = "星级酒店评价", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(starhotelreviewsService.deleteStarhotelreviewsByIds(ids));
    }
}
